import * as React from 'react';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import AddIcon from '@mui/icons-material/Add';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/DeleteOutlined';
import SaveIcon from '@mui/icons-material/Save';
import CancelIcon from '@mui/icons-material/Close';
import axios from 'axios'; 
import {
  GridRowModes,
  DataGrid,
  GridToolbarContainer,
  GridActionsCellItem,
  GridRowEditStopReasons,
} from '@mui/x-data-grid';
import {
  randomId,
} from '@mui/x-data-grid-generator';

function EditToolbar(props) {
  const { setRows, setRowModesModel } = props;

  const handleClick = () => {
    const id = randomId()
    setRows((oldRows) => [...oldRows, { id, isNew: true }]);
    setRowModesModel((oldModel) => ({
      ...oldModel,
      [id]: { mode: GridRowModes.Edit, fieldToFocus: 'player_id' },
    }));
  };

  return (
    // remove button functionality for add until it works
    <GridToolbarContainer>
      <Button color="primary" startIcon={<AddIcon />}>
        Add record
      </Button>
    </GridToolbarContainer>
  );
}

export default function FullFeaturedCrudGrid() {
  const [rows, setRows] = React.useState([]);
  const [rowModesModel, setRowModesModel] = React.useState({});
  const [playerOptions, setPlayerOptions] = React.useState([]);
  const [gameOptions, setGameOptions] = React.useState([]);

    // Function to fetch the initial data from the server using Axios
    const fetchInitialData = async () => {
      try {
        const response = await axios.get('/stats/get_stats'); // Use Axios for the GET request
        if (response.status === 200) {
          const data = response.data;
          // Assign unique IDs to each row using randomId()
          const rowsWithIds = data.map((row) => ({ id: randomId(), ...row }));
          setRows(rowsWithIds);
        } else {
          console.error('Failed to fetch initial data');
        }
      } catch (error) {
        console.error('Error fetching initial data:', error);
      }
    };

      // Function to fetch player data from the API and create mapping from id to name
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

      // Function to fetch game data from the API and create mapping from id to game info
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
            console.error('Error fetching dat data:', error);
          });
      };
  
    React.useEffect(() => {
      fetchInitialData();
      fetchPlayerData();
      fetchGameData();
    }, []);

  const handleRowEditStop = (params, event) => {
    if (params.reason === GridRowEditStopReasons.rowFocusOut) {
      event.defaultMuiPrevented = true;
    }
  };

  const handleEditClick = (id) => () => {
    setRowModesModel({ ...rowModesModel, [id]: { mode: GridRowModes.Edit } });
  };

  const handleSaveClick = (id) => () => {
    setRowModesModel({ ...rowModesModel, [id]: { mode: GridRowModes.View } });
  };

  const handleDeleteClick = (id) => async () => {
    const rowToDelete = rows.find((row) => row.id === id);
    if (rowToDelete) {
      const { player_id, game_id } = rowToDelete;
  
      try {
        await axios.delete('/stats/delete_stats', {
          data: { 'player_id': player_id, 'game_id': game_id },
        });
        // If the delete request is successful, update the table to reflect the changes
        setRows((currentRows) =>
          currentRows.filter((row) => row.id !== id)
        );
      } catch (error) {
        console.error('Error deleting row:', error);
      }
    }
  };
  

  const handleCancelClick = (id) => () => {
    setRowModesModel({
      ...rowModesModel,
      [id]: { mode: GridRowModes.View, ignoreModifications: true },
    });

    const editedRow = rows.find((row) => row.id === id);
    if (editedRow.isNew) {
      setRows(rows.filter((row) => row.id !== id));
    }
  };

  const processRowUpdate = (newRow) => {
    if (newRow) {
      const { id, player_id, game_id, points, assists, rebounds, blocks, steals } = newRow;
      try {
        axios.put('/stats/edit_stats', {
          'player_id': player_id, 
          'game_id': game_id,
          'points': points,
          'assists': assists,
          'rebounds': rebounds,
          'blocks': blocks,
          'steals': steals 
        });
        // If the update request is successful, update the table to reflect the changes
        const updatedRow = { ...newRow, isNew: false };
        setRows(rows.map((row) => (row.id === newRow.id ? updatedRow : row)));
        return updatedRow;
      } catch (error) {
        console.error('Error deleting row:', error);
        throw error
      }
    }
  };

  const handleRowModesModelChange = (newRowModesModel) => {
    setRowModesModel(newRowModesModel);
  };

  const columns = [
    { field: 'player_id', 
      headerName: 'Player', 
      width: 200, 
      align: 'left',
      headerAlign: 'left',
      editable: false,
      type: 'singleSelect', 
      valueOptions: playerOptions
    },
    {
      field: 'game_id',
      headerName: 'Game',
      width: 400,
      align: 'left',
      headerAlign: 'left',
      editable: false,
      type: 'singleSelect',
      valueOptions: gameOptions
    },
    {
      field: 'points',
      headerName: 'PTS',
      type: 'number',
      width: 100,
      align: 'left',
      headerAlign: 'left',
      editable: true,
    },
    {
      field: 'assists',
      headerName: 'AST',
      type: 'number',
      width: 100,
      align: 'left',
      headerAlign: 'left',
      editable: true,
    },
    {
      field: 'rebounds',
      headerName: 'REB',
      type: 'number',
      width: 100,
      align: 'left',
      headerAlign: 'left',
      editable: true,
    },
    {
      field: 'blocks',
      headerName: 'BLK',
      type: 'number',
      width: 100,
      align: 'left',
      headerAlign: 'left',
      editable: true,
    },
    {
      field: 'steals',
      headerName: 'STL',
      type: 'number',
      width: 100,
      align: 'left',
      headerAlign: 'left',
      editable: true,
    },
    {
      field: 'actions',
      type: 'actions',
      headerName: 'Actions',
      width: 100,
      cellClassName: 'actions',
      getActions: ({ id }) => {
        const isInEditMode = rowModesModel[id]?.mode === GridRowModes.Edit;

        if (isInEditMode) {
          return [
            <GridActionsCellItem
              icon={<SaveIcon />}
              label="Save"
              sx={{
                color: 'primary.main',
              }}
              onClick={handleSaveClick(id)}
            />,
            <GridActionsCellItem
              icon={<CancelIcon />}
              label="Cancel"
              className="textPrimary"
              onClick={handleCancelClick(id)}
              color="inherit"
            />,
          ];
        }

        return [
          <GridActionsCellItem
            icon={<EditIcon />}
            label="Edit"
            className="textPrimary"
            onClick={handleEditClick(id)}
            color="inherit"
          />,
          <GridActionsCellItem
            icon={<DeleteIcon />}
            label="Delete"
            onClick={handleDeleteClick(id)}
            color="inherit"
          />,
        ];
      },
    },
  ];

  return (
    <Box
      sx={{
        height: 500,
        width: '100%',
        '& .actions': {
          color: 'text.secondary',
        },
        '& .textPrimary': {
          color: 'text.primary',
        },
      }}
    >
      <DataGrid
        rows={rows}
        columns={columns}
        editMode="row"
        rowModesModel={rowModesModel}
        onRowModesModelChange={handleRowModesModelChange}
        onRowEditStop={handleRowEditStop}
        processRowUpdate={processRowUpdate}
        onProcessRowUpdateError={(error) => {
          // Handle the error here, e.g., display a message to the user or log it.
          console.error('Error updating row:', error);
          fetchInitialData();
        }}
        slots={{
          toolbar: EditToolbar,
        }}
        slotProps={{
          toolbar: { setRows, setRowModesModel },
        }}
      />
    </Box>
  );
}