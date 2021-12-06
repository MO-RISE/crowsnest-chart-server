
FROM maptiler/tileserver-gl

# Install Python (needed for the modfiy_style_specs.py script)
USER root
RUN apt update && apt upgrade -y
RUN apt install -y python3

WORKDIR /data
COPY start.sh .
COPY styles styles
COPY config.json .
RUN chmod +x start.sh
RUN chmod -R a+rwx styles 
COPY modify_style_specs.py .

USER node:node

ENTRYPOINT ["/data/start.sh"]

#CMD ["-p", "80"]
