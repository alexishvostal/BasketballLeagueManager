import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { InputLabel, MenuItem, FormControl, Select } from '@mui/material';

export default function TeamDropdown({ selectedTeam, setSelectedTeam }) {
  const [teamOptions, setTeamOptions] = useState([]);

  // Function to fetch team data from the API
  const fetchTeamData = () => {
    axios.get('/team/get_teams')
      .then((response) => {
        if (Array.isArray(response.data)) {
          const options = response.data.map((team) => ({
            // Label for each team id should be the team name
            value: team.team_id,
            label: `${team.name}`,
          }));
          setTeamOptions(options);
        }
      })
      .catch((error) => {
        console.error('Error fetching team data:', error);
      });
  };

  useEffect(() => {
    fetchTeamData()
  }, []);

  return (

    <FormControl fullWidth>
      <InputLabel id="team-label">Team</InputLabel>
      <Select
        labelId="team-label"
        id="team-select"
        value={selectedTeam}
        label="Team"
        onChange={(e) => setSelectedTeam(e.target.value)}
        required
      >
        {teamOptions.map((team) => (
          <MenuItem key={team.value} value={team.value}>
            {team.label}
          </MenuItem>
        ))}
      </Select>
    </FormControl>

  );
}