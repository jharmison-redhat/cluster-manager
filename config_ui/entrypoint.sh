#!/bin/sh

cat << 'EOF' | python3
from faros_config_ui.app import app
app.run()
EOF
