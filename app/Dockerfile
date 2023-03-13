# Basics.
FROM python:3.10-buster
WORKDIR /app

# Update the container.
RUN apt-get update
RUN apt-get upgrade -y

# Create the user.
RUN useradd -m user
RUN chown -R user /app

# Install the packages.
USER user
COPY --chown=user requirements.txt ./
RUN pip3 install -r requirements.txt

# Copy the public folder
COPY --chown=user public ./public

# Copy the project
COPY --chown=user src ./src

# Run the project
CMD python3 -u ./src/main.py
