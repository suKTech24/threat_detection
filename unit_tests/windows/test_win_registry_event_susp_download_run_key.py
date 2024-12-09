import pytest

@pytest.fixture
def mock_data():
    """
    Returns mock data for the detection rule in a Python list format.
    """
    return [
        {'event_id': 1, 'process_executable': '/downloads/malicious.exe', 'registry_path': '/software/microsoft/windows/currentversion/run/'},
        {'event_id': 2, 'process_executable': '/downloads/safe_file.exe', 'registry_path': '/software/microsoft/windows/currentversion/run/'},
        {'event_id': 3, 'process_executable': '/other_folder/benign.exe', 'registry_path': '/software/microsoft/windows/currentversion/run/'},
        {'event_id': 4, 'process_executable': '/downloads/malicious.exe', 'registry_path': '/some/other/path/'},
        {'event_id': 5, 'process_executable': '/temporary internet files/content.outlook/file.exe', 'registry_path': '/software/microsoft/windows/currentversion/run/'},
    ]

def matches_detection_logic(row):
    """
    Simulates the detection rule logic in Python.
    """
    executable_patterns = [
        '/downloads/',
        '/temporary internet files/content.outlook/',
        '/local settings/temporary internet files/'
    ]
    return (
        any(pattern in row['process_executable'] for pattern in executable_patterns)
        and '/software/microsoft/windows/currentversion/run/' in row['registry_path']
    )

def test_detection_rule(mock_data):
    """
    Validates the detection rule logic directly using Python filtering.
    """
    # Simulate filtering logic
    filtered_rows = [row for row in mock_data if matches_detection_logic(row)]

    # Extract the IDs of rows that match the WHERE clause
    actual_event_ids = {row['event_id'] for row in filtered_rows}

    # Expected event IDs based on the detection rule's logic
    expected_event_ids = {1, 2, 5}

    assert actual_event_ids == expected_event_ids, f"Expected {expected_event_ids}, but got {actual_event_ids}"
