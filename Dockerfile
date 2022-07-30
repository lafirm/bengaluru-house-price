FROM python:3.10.5 as build-stage
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE $PORT
RUN chown -R python .
RUN python build
CMD gunicorn --bind 0.0.0.0:$PORT app:app

FROM nginx:alpine
COPY --from=build-stage /app/client/ /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
CMD sed -i -e 's/$PORT/'"$PORT"'/g' /etc/nginx/conf.d/default.conf && nginx -g 'daemon off;'