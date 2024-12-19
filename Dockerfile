# Define base image
FROM continuumio/miniconda3
 
# Set working directory for the project
WORKDIR /app

# Install system dependencies, including libGL
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    && apt-get clean

# Create Conda environment from the YAML file
COPY environment.yml .
RUN conda env create -f environment.yml && conda clean -afy
 
# Override default shell and use bash
SHELL ["conda", "run", "-n", "yolov5", "/bin/bash", "-c"]
 
# Activate Conda environment and check if it is working properly
RUN echo "Making sure flask is installed correctly..."
RUN python -c "import flask"
 
# Python program to run in the container
COPY app.py .
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "yolov5", "python", "app.py"]