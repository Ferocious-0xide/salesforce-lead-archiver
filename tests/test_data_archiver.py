import unittest
from unittest.mock import patch, MagicMock
from data_archiver import connect_to_db, archive_data, LEAD_OBJECT

class TestDataArchiver(unittest.TestCase):

    @patch('data_archiver.psycopg2.connect')
    def test_connect_to_db(self, mock_connect):
        connect_to_db('dummy_url')
        mock_connect.assert_called_once_with('dummy_url')

    @patch('data_archiver.connect_to_db')
    def test_archive_data(self, mock_connect):
        # Mock the database connections and cursors
        mock_source_conn = MagicMock()
        mock_dest_conn = MagicMock()
        mock_source_cursor = MagicMock()
        mock_dest_cursor = MagicMock()
        mock_source_conn.cursor.return_value = mock_source_cursor
        mock_dest_conn.cursor.return_value = mock_dest_cursor

        # Mock the fetchall method to return some test data
        mock_source_cursor.fetchall.return_value = [
            ('1', True, 'Doe', 'John', 'John Doe', 'TestCo', 'City', 'State', '12345', 
             '1234567890', '0987654321', '1122334455', 'john@test.com', 'www.test.com', 
             'Description', 'Industry', '2023-01-01', '2023-01-01', 'EXT001')
        ]

        # Call the function
        archive_data(mock_source_conn, mock_dest_conn)

        # Assert that the correct SQL was executed
        mock_source_cursor.execute.assert_called_once()
        mock_dest_cursor.executemany.assert_called_once()

        # You can add more specific assertions here based on your needs

if __name__ == '__main__':
    unittest.main()