FROM nginx:1.15
COPY ./sites-enabled/demo /etc/nginx/sites-enabled/demo
# RUN ln -s /etc/nginx/sites-available/demo /etc/nginx/sites-enabled
RUN systemctl restart nginx