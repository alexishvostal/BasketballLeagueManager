import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Box from '@mui/material/Box';
import {
  DataGrid,
} from '@mui/x-data-grid';
import {
  randomId,
} from '@mui/x-data-grid-generator';

export default function TeamRoster({selectedTeam}) {
  const [rows, setRows] = useState([]);

  // Function to fetch team roster from API
  const fetchTeamRoster = async () => {
    try {
      const response = await axios.get('/report/get_roster', {
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
    fetchTeamRoster()
  }, [selectedTeam]);

  const columns = [
    { field: 'player_name', 
      headerName: 'Player', 
      width: 200, 
      align: 'left',
      headerAlign: 'left'
    },
    {
      field: 'ppg',
      headerName: 'PPG',
      type: 'number',
      width: 100,
      align: 'left',
      headerAlign: 'left'
    },
    {
      field: 'apg',
      headerName: 'APG',
      type: 'number',
      width: 100,
      align: 'left',
      headerAlign: 'left'
    },
    {
      field: 'rpg',
      headerName: 'RPG',
      type: 'number',
      width: 100,
      align: 'left',
      headerAlign: 'left'
    },
    {
      field: 'bpg',
      headerName: 'BPG',
      type: 'number',
      width: 100,
      align: 'left',
      headerAlign: 'left'
    },
    {
      field: 'spg',
      headerName: 'SPG',
      type: 'number',
      width: 100,
      align: 'left',
      headerAlign: 'left'
    }
  ];

  return (
    <div>
      <h3>Roster</h3>
      <Box
        sx={{
          height: 380,
          width: '100%',
        }}
      >
        <DataGrid
          rows={rows}
          columns={columns}
        />
      </Box>
    </div>
  );
};