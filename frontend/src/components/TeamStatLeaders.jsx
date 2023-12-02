import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Box from '@mui/material/Box';
import {
  DataGrid,
} from '@mui/x-data-grid';
import {
  randomId,
} from '@mui/x-data-grid-generator';

export default function TeamStatLeaders({selectedTeam}) {
  const [rows, setRows] = useState([]);

  // Function to fetch team stats leaders from API
  const fetchStatsLeaders = async () => {
    try {
      const response = await axios.get('/report/get_stats_leaders', {
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
    fetchStatsLeaders()
  }, [selectedTeam]);

  const columns = [
    { field: 'stat_category', 
      headerName: 'Stat', 
      width: 100, 
      align: 'left',
      headerAlign: 'left'
    },
    {
      field: 'player_name',
      headerName: 'Player',
      width: 200,
      align: 'left',
      headerAlign: 'left'
    }
  ];

  return (
    <Box
      sx={{
        height: 375,
        width: 310,
      }}
    >
      <DataGrid
        rows={rows}
        columns={columns}
        pageSize={5}
        pageSizeOptions={[5]}
      />
    </Box>
  );
};