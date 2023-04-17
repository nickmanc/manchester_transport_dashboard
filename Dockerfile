# app/Dockerfile

FROM python:3.9-slim

WORKDIR /app

ARG DASHBOARD_BUILD_VERSION
ARG GOOGLE_ANALYTICS_TAG

ENV DASHBOARD_BUILD_VERSION=${DASHBOARD_BUILD_VERSION:-NOT_DEFINED}
ENV GOOGLE_ANALYTICS_TAG=${GOOGLE_ANALYTICS_TAG:-"G-XXXXXXXX"}

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm  \
    -rf /var/lib/apt/lists/*

COPY . .

RUN pip3 install -r requirements.txt

RUN export STREAMLIT_LOCATION=$(pip3 show streamlit | grep Location | awk '{print $2}') && \
    sed -i "s/<head>/<head>\n<!-- Google Analytics -->\n<script async src=\"https:\/\/www.googletagmanager.com\/gtag\/js?id=${GOOGLE_ANALYTICS_TAG}\"><\/script>\n<script>\n\twindow.dataLayer = window.dataLayer || [];\n\tfunction gtag() {dataLayer.push(arguments);}\n\tgtag('js', new Date());\n\tgtag('config', '${GOOGLE_ANALYTICS_TAG}');\n<\/script>\n/g" $STREAMLIT_LOCATION/streamlit/static/index.html

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]