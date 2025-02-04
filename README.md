# Discord Last Seen Bot

This bot tracks the online/offline status of specified Discord users and notifies a designated user when their status changes.

## Features

- Tracks the online/offline status of specified users.
- Sends notifications to a designated user when tracked users go online or offline.
- Stores the last seen time of tracked users in a SQLite database.

## Requirements

- Python 3.11
- Docker (optional, for containerized deployment)

## Setup

### Environment Variables

Create a `.env` file in the root directory with the following content:

```
DISCORD_TOKEN=YOUR_DISCORD_BOT_TOKEN
TRACKED_USERS=TRACKED_USERS_ID_SEPARATED_BY_COMMA
NOTIFICATION_USER=SINGLE_USER_ID_FOR_NOTIFICATIONS
```

### Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### Database Setup

The bot will automatically create a SQLite database named `last_seen.db` in the root directory.

## Running the Bot

### Locally

Run the bot using Python:

```bash
python index.py
```

### Using Docker

Build and run the Docker container:

```bash
docker-compose up --build
```

## Usage

### Commands

- `@PINGBOT lastseen [user]`: Displays the last seen time of the specified user. If no user is specified, it displays the last seen times of all tracked users.

### Events

- The bot will automatically track the online/offline status of users specified in the `TRACKED_USERS` environment variable and notify the user specified in the `NOTIFICATION_USER` environment variable.

## Contributing

Feel free to submit issues or pull requests if you have any improvements or bug fixes.

## License

This project is licensed under the MIT License.
