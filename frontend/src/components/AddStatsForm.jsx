import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { TextField, Stack, Button, MenuItem, Select, InputLabel, FormControl } from '@mui/material';

const RegisterForm = () => {
  const [selectedPlayer, setSelectedPlayer] = useState('');
  const [selectedGame, setSelectedGame] = useState('');
  const [points, setPoints] = useState('');
  const [assists, setAssists] = useState('');
  const [rebounds, setRebounds] = useState('');
  const [blocks, setBlocks] = useState('');
  const [steals, setSteals] = useState('');


  const [playerOptions, setPlayerOptions] = useState([]);
  const [gameOptions, setGameOptions] = useState([]);

  // Function to fetch player data from the API
  const fetchPlayerData = () => {
    axios.get('/player/get_players')
      .then((response) => {
        if (Array.isArray(response.data)) {
          const options = response.data.map((player) => ({
            // Label for each player id should be the player's name
            value: player.player_id,
            label: `${player.first_name} ${player.last_name}`,
          }));
          setPlayerOptions(options);
        }
      })
      .catch((error) => {
        console.error('Error fetching player data:', error);
      });
  };

  // Function to fetch game data from the API
  const fetchGameData = () => {
    axios.get('/game/get_games')
      .then((response) => {
        if (Array.isArray(response.data)) {
          const options = response.data.map((game) => ({
            // Label for each game id should be date, time, location for game
            value: game.game_id,
            label: `Date: ${game.date} | Time: ${game.time} | Location: ${game.location}`,
          }));
          setGameOptions(options);
        }
      })
      .catch((error) => {
        console.error('Error fetching game data:', error);
      });
  };
  
  useEffect(() => {
    fetchPlayerData();
    fetchGameData();
  }, []);

  function handleSubmit(event) {
    event.preventDefault();
    console.log(selectedPlayer, selectedGame, points, assists, rebounds, blocks, steals);

    axios.post('/stats/add_stats', {
      'player_id': selectedPlayer,
      'game_id': selectedGame,
      'points': points,
      'assists': assists,
      'rebounds': rebounds,
      'blocks': blocks,
      'steals': steals
    })
      .then((response) => {
        console.log("Successfully added row:", response.data);
      })
      .catch((error) => {
        console.error('Error adding row:', error);
        console.error('Record already exists in the database.');
      })
      .finally(() => {
        // Clear form regardless of successful completion
        setSelectedPlayer('');
        setSelectedGame('');
        setPoints('');
        setAssists('');
        setRebounds('');
        setBlocks('');
        setSteals('');
      });

  }

  return (
    <div>
      <h2>Add Player Game Stats Form</h2>
      <form onSubmit={handleSubmit}>
        
        <FormControl fullWidth sx={{ mb: 4 }}>
          <InputLabel id="player-label">Player</InputLabel>
          <Select
            labelId="player-label"
            id="player-select"
            value={selectedPlayer}
            label="Player"
            onChange={(e) => setSelectedPlayer(e.target.value)}
            required
          >
            {playerOptions.map((player) => (
              <MenuItem key={player.value} value={player.value}>
                {player.label}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
        <FormControl fullWidth sx={{ mb: 4 }}>
          <InputLabel id="game-label">Game</InputLabel>
          <Select
            labelId="game-label"
            id="game-select"
            value={selectedGame}
            label="Game"
            onChange={(e) => setSelectedGame(e.target.value)}
            required
          >
            {gameOptions.map((game) => (
              <MenuItem key={game.value} value={game.value}>
                {game.label}
              </MenuItem>
            ))}
          </Select>
        </FormControl>

        <Stack spacing={5} direction="row" sx={{marginBottom: 4}}>
          <TextField
            type="number"
            label={points ? null : "PTS"}
            onChange={(e) => setPoints(e.target.value)}
            value={points}
            fullWidth
            required
          />
          <TextField
            type="number"
            label={assists ? null : "AST"}
            onChange={(e) => setAssists(e.target.value)}
            value={assists}
            fullWidth
            required
          />
          <TextField
            type="number"
            label={rebounds ? null : "REB"}
            onChange={(e) => setRebounds(e.target.value)}
            value={rebounds}
            fullWidth
            required
          />
          <TextField
            type="number"
            label={blocks ? null : "BLK"}
            onChange={(e) => setBlocks(e.target.value)}
            value={blocks}
            fullWidth
            required
          />
          <TextField
            type="number"
            label={steals ? null : "STL"}
            onChange={(e) => setSteals(e.target.value)}
            value={steals}
            fullWidth
            required
          />
        </Stack>

        <Button variant="outlined" type="submit">
          Add Record
        </Button>
      </form>
      {/* Optionally, you can add a message here */}
    </div>
  );
};

export default RegisterForm;