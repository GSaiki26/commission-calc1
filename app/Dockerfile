# Basics.
FROM python:3.10-alpine
WORKDIR /app

# Update the container.
RUN apk update
RUN apk upgrade

# Create the user.
RUN adduser -D user
RUN chown -R user /app

# Install the packages.
USER user
COPY --chown=user requirements.txt ./
RUN pip3 install -r requirements.txt

# Copy the project
COPY --chown=user src ./src

# Run the project
CMD python3 -u ./src/main.py
