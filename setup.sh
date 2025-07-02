#!/bin/bash
echo "🔧 Setting up Git filters for Jupyter notebooks..."

# Check if nbstripout is installed on host
if ! command -v nbstripout &> /dev/null; then
    echo "Installing nbstripout on host..."
    pip install nbstripout
else
    echo "nbstripout already installed"
fi

# Configure git filters
echo "Configuring git filters..."
nbstripout --install --attributes .gitattributes --keep-output

echo "Building Docker image..."
docker-compose build

echo "✅ Setup complete!"
echo "✅ Run: docker-compose up"