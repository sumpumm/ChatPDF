import streamlit as st
import streamlit_authenticator as stauth


hashed=stauth.Hasher(["admin"]).generate()

print(hashed)