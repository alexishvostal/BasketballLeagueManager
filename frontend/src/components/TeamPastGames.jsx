import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Box from '@mui/material/Box';
import {
  DataGrid,
} from '@mui/x-data-grid';
import {
  randomId,
} from '@mui/x-data-grid-generator';

export default function TeamPastGames({selectedTeam}) {
  const [rows, setRows] = useState([]);

  // Function to fetch team past game results from API
  const fetchPastGames = async () => {
    try {
      const response = await axios.get('/report/get_past_games', {
        params: {
          team_id: String(selectedTeam)
        }
      });

      if (response.status === 200) {
        const data = response.data;
        const rowsWithIds = data.map((row) => ({ id: randomId(), ...row }));
        setRows(rowsWithIds);
      } else {
        console.error('Failed to fetch initial data');
      }
    } catch (error) {
      console.error("Error fetching win-loss record: ", error);
    }
  };

  useEffect(() => {
    fetchPastGames()
  }, [selectedTeam]);

  const columns = [
    { field: 'date', 
      headerName: 'Date', 
      width: 100, 
      align: 'left',
      headerAlign: 'left'
    },
    {
      field: 'opponent',
      headerName: 'Opponent',
      width: 200,
      align: 'left',
      headerAlign: 'left'
    },
    {
      field: 'score',
      headerName: 'Score',
      width: 100,
      align: 'left',
      headerAlign: 'left'
    },
    {
      field: 'wl',
      headerName: 'W/L',
      width: 50,
      align: 'left',
      headerAlign: 'left'
    }
  ];

  return (
    <Box
      sx={{
        height: 215,
        width: 460,
      }}
    >
      <DataGrid
        rows={rows}
        columns={columns}
        autoPageSize={true}
      />
    </Box>
  );
};