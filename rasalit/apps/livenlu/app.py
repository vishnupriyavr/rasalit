import pathlib
import argparse

import pandas as pd
import streamlit as st

from rasalit.apps.livenlu.common import (
    load_interpreter,
    create_altair_chart,
    create_displacy_chart,
    fetch_info_from_message,
)

parser = argparse.ArgumentParser(description="")
parser.add_argument("--folder", help="Pass the model folder.")
args = parser.parse_args()

model_folder = args.folder


st.markdown("# Arabic KYC NLU Model Summary")
st.markdown("You can select a model on the left to interact with.")

model_files = [str(p.parts[-1]) for p in pathlib.Path(model_folder).glob("*.tar.gz")]
model_file = st.sidebar.selectbox("What model do you want to use", model_files)

interpreter = load_interpreter(model_folder, model_file)

text_input = st.text_input("Text Input for Model", "Hello")

blob, nlu_dict, tokens = fetch_info_from_message(
    interpreter=interpreter, text_input=text_input
)

st.markdown("## Tokens and Entities")
st.write(
    create_displacy_chart(tokens=tokens, entities=nlu_dict["entities"]),
    unsafe_allow_html=True,
)

st.markdown("## Intents")

chart_data = pd.DataFrame(blob["intent_ranking"]).sort_values("name")
p = create_altair_chart(chart_data)
st.altair_chart(p.properties(width=600))
