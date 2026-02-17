import streamlit as st
from kick_client.auth import build_authorize_url, exchange_code_for_token, refresh_access_token
from kick_client.data import get_me, get_channels

def _first(v):
    return v[0] if isinstance(v, list) else v

@st.cache_resource
def pkce_pending() -> dict:
    # state -> verifier
    return {}

def run():
    st.title("PeekKick")

    if st.button("Zaloguj przez Kick"):
        auth_url, verifier, state = build_authorize_url()
        pkce_pending()[state] = verifier   # <-- kluczowe: działa między sesjami/kartami
        st.session_state.auth_url = auth_url
        st.code(auth_url)

    if st.session_state.get("auth_url"):
        st.markdown(f"[Przejdź do Kick (autoryzacja)]({st.session_state.auth_url})")

    qp = st.query_params
    code = _first(qp.get("code"))
    returned_state = _first(qp.get("state"))

    if code and returned_state:
        verifier = pkce_pending().pop(returned_state, None)
        if not verifier:
            st.error("Nie mam verifier dla tego state (kliknij login jeszcze raz).")
            st.stop()

        token = exchange_code_for_token(code, verifier)  # <-- redirect_uri stałe z env
        st.session_state.token = token

        st.query_params.clear()
        st.rerun()

    if "token" in st.session_state:
        st.success("Mam tokeny 🎉")
        #st.json(st.session_state.token)

        access_token = st.session_state.token.get("access_token")
        st.code(access_token[:8] + "...")

        if st.button("Pobierz moj profil z Kick"):
            with st.spinner("Pobieram dane z Kick API..."):
                me = get_me(access_token)
            st.json(me)
        if st.button("Odswiez access token"):
            new_token = refresh_access_token(st.session_state.token["refresh_token"])
            st.session_state.token = new_token

            st.success("Odswiezone")
        if st.button("Pobierz kanal Kick"):
            with st.spinner("Pobieram dane z Kick API..."):
                channels = get_channels(access_token, is_live = True, limit = 10)
            for ch in channels.get("data", []):
                st.subheader(ch["slug"])
                st.write(f"👥 Viewers: {ch.get('viewer_count')}")
                st.write(f"🔴 Live: {ch.get('is_live')}")
                st.divider()