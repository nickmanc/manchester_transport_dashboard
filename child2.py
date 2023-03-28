import os

import streamlit as st
from datetime import datetime
from streamlit_autorefresh import st_autorefresh
from trams import get_tram_departures

NO_TRAM_SCHEDULED_MESSAGE = "No trams currently scheduled to depart."

#dashboard just for child 2

st.set_page_config(layout="wide")
# get rid of massive blank header
st.markdown(
    """
        <style>
            .appview-container .main .block-container {{
                padding-top: {padding_top}rem;
                padding-bottom: {padding_bottom}rem;
                }}

        </style>""".format(
        padding_top=0, padding_bottom=1
    ),
    unsafe_allow_html=True,
)

# st_autorefresh(interval=60 * 1000)
st_autorefresh(interval=15 * 1000)

#if before 11am
if datetime.now().hour < 11:
    from_container = st.container()
    # Display tram information in a table
    from_container.subheader(f'[{os.environ["child2_morning_name"]}]({os.environ["child2_morning_url"]})')
    tramDepartureInfo = get_tram_departures({os.environ["child2_morning_ids"]})
    trams = tramDepartureInfo[0]
    if len(trams) > 0:
        for tram in trams:
            if tram['expected'] == 0:
                tramExpectedText = "NOW"
            else:
                tramExpectedText = f"in **{tram['expected']}** minutes."
            from_container.markdown(f"**{tram['destination']}**  ({tram['carriages']}) **{tramExpectedText}**")
    else:
        from_container.markdown(NO_TRAM_SCHEDULED_MESSAGE)

to_container = st.container()
to_container.subheader(f'[{os.environ["child2_afternoon_name"]}]({os.environ["child2_afternoon_url"]})')
tramDepartureInfo = get_tram_departures({os.environ["child2_afternoon_ids"]})
trams = tramDepartureInfo[0]
if len(trams) > 0:
    for tram in trams:
        if tram['expected'] == 0:
            tramExpectedText = "NOW"
        else:
            tramExpectedText = f"in **{tram['expected']}** minutes."
        to_container.markdown(f"**{tram['destination']}**  ({tram['carriages']}) **{tramExpectedText}**")
else:
    to_container.markdown(NO_TRAM_SCHEDULED_MESSAGE)


#if after 11am
if datetime.now().hour >= 11:
    from_container = st.container()
    # Display tram information in a table
    from_container.subheader(f'[{os.environ["child2_morning_name"]}]({os.environ["child2_morning_url"]})')
    tramDepartureInfo = get_tram_departures({os.environ["child2_morning_ids"]})
    trams = tramDepartureInfo[0]
    if len(trams) > 0:
        for tram in trams:
            if tram['expected'] == 0:
                tramExpectedText = "NOW"
            else:
                tramExpectedText = f"in **{tram['expected']}** minutes."
            from_container.markdown(f"**{tram['destination']}**  ({tram['carriages']}) **{tramExpectedText}**")
    else:
        from_container.markdown(NO_TRAM_SCHEDULED_MESSAGE)


footer = f"""<style>
  .footer {{
    display: flex; /* display the elements in a row */
    justify-content: space-between; /* space the elements evenly */
    align-items: center; /* center the items vertically */
    padding: 10px 0; /* add some padding to the top and bottom */
    width: 100%; /* set the width to 100% */
    color: grey;
    justify-content: space-around;
  }}
  
  .footer td {{
    border: none; /* remove the borders from the table cells */
  }}
</style>
<div class="footer">
  <table>
    <tr>
      <td>Last updated: {datetime.now().strftime('%H:%M:%S')}</td>
      <td>Contains Transport for Greater Manchester data</td>
    </tr>
  </table>
</div>
"""
st.markdown(footer, unsafe_allow_html=True)
