#!/bin/bash

echo "=========================================="
echo "  TAR ESCAPE CHALLENGE - Setup Script"
echo "=========================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "[ERROR] Docker is not installed. Please install Docker first."
    echo ""
    echo "Install Docker:"
    echo "  Ubuntu/Debian: sudo apt-get install docker.io"
    echo "  macOS: brew install --cask docker"
    echo "  Or visit: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker daemon is running
if ! docker info &> /dev/null; then
    echo "[ERROR] Docker daemon is not running."
    echo "Please start Docker and try again."
    exit 1
fi

echo "[*] Docker detected and running..."
echo ""

# Build the Docker image
echo "[*] Building challenge Docker image..."
echo "    This may take a few minutes on first build..."
echo ""

docker build -t tar-escape-challenge .

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "  BUILD SUCCESSFUL!"
    echo "=========================================="
    echo ""
    echo "Challenge is ready to run!"
    echo ""
    echo "Start the challenge:"
    echo "  docker run -it --rm \\"
    echo "    --security-opt=no-new-privileges \\"
    echo "    --cap-drop=ALL \\"
    echo "    tar-escape-challenge"
    echo "=========================================="
else
    echo ""
    echo "[ERROR] Failed to build Docker image"
    echo "Please check the error messages above."
    exit 1
fi
