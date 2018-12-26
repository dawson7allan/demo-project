FROM nginx:1.15
RUN rm /etc/nginx/sites-enabled/default
ADD ./sites-enabled/demo /etc/nginx/sites-enabled/demo
CMD ["ln", "-s", "/etc/nginx/sites-available/myproject", "/etc/nginx/sites-enabled"]
CMD ["systemctl", "restart", "nginx"]