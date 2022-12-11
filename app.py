import streamlit as st
import pandas as pd
from st_aggrid import AgGrid
import warnings
import plotly.graph_objects as go

def main():
    st.set_page_config(page_title="CO2", page_icon="🌍", layout="wide")
    warnings.filterwarnings("ignore")
    st.header("🌍📈 CO2 Ausstoß je Land und Jahr")
    hide_streamlit_style = """
           <style>
            div.block-container{padding-top:2rem;}
               div[data-testid="stToolbar"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
             div.block-container{padding-bottom:0rem;}
           </style>
           """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    try:
        df = pd.read_csv(r"https://raw.githubusercontent.com/tobiarnold/CO2-per-Country/main/data.csv")
        df2 = pd.read_csv(r"https://raw.githubusercontent.com/tobiarnold/CO2-per-Country/main/data_graph.csv")
        clist = df["Country"].unique().tolist()
        countries = st.multiselect("Land auswählen", clist,['China','United States','India','Russia','Japan','Germany'])
        config = {"displayModeBar": False}
        dfs = {country: df2[df2["Country"] == country] for country in countries}
        fig = go.Figure()
        for country, df2 in dfs.items():
            fig = fig.add_trace(go.Scatter(x=df2["year"], y=df2["value"], name=country))
        fig.update_layout(height= 600)
        fig.update_layout(margin=dict(l=20, r=0, t=0, b=15))
        fig.update_layout(legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
        st.subheader("Megatonnen CO2-Äquivalent 1850-2019 je Land")
        st.plotly_chart(fig,use_container_width=True, config=config)
        AgGrid(df, height=400)
        st.write("Quelle: Potsdam-Institut für Klimafolgenforschung")
    except:
        st.write("Ein Fehler ist aufgetreten. App bitte neu laden.")

main()
