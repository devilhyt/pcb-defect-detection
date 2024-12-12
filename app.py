import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards
from ultralytics import YOLO
from PIL import Image

# setting the app
st.set_page_config(layout="wide")

style_metric_cards(
    background_color="#262730",
    border_left_color=None,
    border_color=None,
    box_shadow=False,
)


# load and cache the model
@st.cache_resource
def load_model():
    return YOLO("pcb_defect/v3/weights/best.pt")


# a flag to check if the image is updated
def file_uploader_on_change():
    st.session_state["image_updated"] = True


# initilaize the app
if "image_updated" not in st.session_state:
    st.session_state["image_updated"] = True
model = load_model()

# main app
st.title("PCB Defect Detection")
st.divider()
# st.image('./image/pcb.jpg', use_container_width=True)
col1, col2 = st.columns(2, gap="large")

# image uploader
with col1:
    st.header("Choose an PCB image")
    uploaded_file = st.file_uploader(
        "", type=["jpg", "jpeg", "png"], on_change=file_uploader_on_change
    )
    st.divider()

# predict the image only if the image is uploaded and updated
image_updated = st.session_state["image_updated"]
if uploaded_file is None:
    st.session_state["label_count"] = {}
elif image_updated:
    image = Image.open(uploaded_file)
    results = model.predict(image)
    annotated_frame = results[0].plot(line_width=3)

    result_df = results[0].to_df()
    label_count = {}
    if not result_df.empty:
        label_count = result_df.value_counts("name").to_dict()

    st.session_state["image"] = image
    st.session_state["annotated_frame"] = annotated_frame
    st.session_state["label_count"] = label_count
    st.session_state["image_updated"] = False

# Defects Count
COLUMNS = 3
with col1:
    st.header("Defects Count")
    cols = st.columns(COLUMNS)
    label_count: dict = st.session_state["label_count"]
    for i, name in enumerate(model.names.values()):
        with cols[i % COLUMNS]:
            value = label_count.get(name, 0)
            st.metric(label=name, value=value)
    st.divider()

# Fault Points
IMAGE_WIDTH = 480
with col2:
    st.header("Fault Points")
    image_switch = st.checkbox("Show Original Image")

    if uploaded_file is not None:
        if image_switch:
            image = st.session_state["image"]
            st.image(image)
        else:
            annotated_frame = st.session_state["annotated_frame"]
            st.image(annotated_frame)

    st.divider()
