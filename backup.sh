#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Define variables
BACKUP_DIR="/backups"
TIMESTAMP=$(date +"%Y%m%d%H%M%S")
BACKUP_FILE="$BACKUP_DIR/backup_$TIMESTAMP.sql"

# Create backup directory if it does not exist
mkdir -p $BACKUP_DIR

# Backup database
PGPASSWORD="$POSTGRES_PASSWORD" pg_dump -U $POSTGRES_USER -h $POSTGRES_HOST -p $POSTGRES_PORT -d $POSTGRES_DB > "$BACKUP_FILE"

# Optionally, compress the backup
gzip $BACKUP_FILE

echo "Backup created at $BACKUP_FILE.gz"
