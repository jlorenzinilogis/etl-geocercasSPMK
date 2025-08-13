# Project Overview

This project is a Python application designed to manage geofencing events for vehicles. It integrates with an external API to extract geofence event data based on vehicle plates and geofences.

## Files

- **src/main.py**: Contains the main application logic, including functions for extracting, transforming, and loading geofence event data.
- **Jenkinsfile**: Defines the CI/CD pipeline for Jenkins, specifying stages for building, testing, and deploying the application.
- **README.md**: Provides documentation for the project, including setup instructions and usage guidelines.

## Setup Instructions

1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd project-app
   ```

2. **Install dependencies**:
   Ensure you have Python installed, then install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. **Configuration**:
   Update the database connection details in `src/main.py` as necessary.

## Usage

To run the application, execute the following command:
```
python src/main.py
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.