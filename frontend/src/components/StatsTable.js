import * as React from 'react';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import AddIcon from '@mui/icons-material/Add';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/DeleteOutlined';
import SaveIcon from '@mui/icons-material/Save';
import CancelIcon from '@mui/icons-material/Close';
import axios from 'axios'; // Import Axios
import {
  GridRowModes,
  DataGrid,
  GridToolbarContainer,
  GridActionsCellItem,
  GridRowEditStopReasons,
} from '@mui/x-data-grid';
import {
  randomCreatedDate,
  randomTraderName,
  randomId,
  randomArrayItem,
} from '@mui/x-data-grid-generator';

const roles = ['Market', 'Finance', 'Development'];
const randomRole = () => {
  return randomArrayItem(roles);
};

const player_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
const game_ids = [1];

const initialRows = [
  {
    id: randomId(),
    player_id: 1,
    game_id: 1,
    points: 16,
    assists: 3,
    rebounds: 4,
    blocks: 0,
    steals: 0
  },
  {
    id: randomId(),
    player_id: 6,
    game_id: 1,
    points: 31,
    assists: 10,
    rebounds: 5,
    blocks: 2,
    steals: 1
  }
];

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
    <GridToolbarContainer>
      <Button color="primary" startIcon={<AddIcon />} onClick={handleClick}>
        Add record
      </Button>
    </GridToolbarContainer>
  );
}

export default function FullFeaturedCrudGrid() {
  const [rows, setRows] = React.useState([]);
  const [rowModesModel, setRowModesModel] = React.useState({});

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
  
    React.useEffect(() => {
      fetchInitialData();
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
    // Find the row in the current rows based on the id
    const rowToDelete = rows.find((row) => row.id === id);
  
    if (rowToDelete) {
      const { player_id, game_id } = rowToDelete;
  
      try {
        // Send a DELETE request to the server to delete the row with the specified player_id and game_id
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
    const updatedRow = { ...newRow, isNew: false };
    setRows(rows.map((row) => (row.id === newRow.id ? updatedRow : row)));
    return updatedRow;
  };

  const handleRowModesModelChange = (newRowModesModel) => {
    setRowModesModel(newRowModesModel);
  };

  const columns = [
    { field: 'player_id', 
      headerName: 'player_id', 
      width: 100, 
      align: 'left',
      headerAlign: 'left',
      editable: true,
      type: 'singleSelect', 
      valueOptions: player_ids 
    },
    {
      field: 'game_id',
      headerName: 'game_id',
      width: 100,
      align: 'left',
      headerAlign: 'left',
      editable: true,
      type: 'singleSelect',
      valueOptions: game_ids
    },
    {
      field: 'points',
      headerName: 'points',
      type: 'number',
      width: 100,
      align: 'left',
      headerAlign: 'left',
      editable: true,
    },
    {
      field: 'assists',
      headerName: 'assists',
      type: 'number',
      width: 100,
      align: 'left',
      headerAlign: 'left',
      editable: true,
    },
    {
      field: 'rebounds',
      headerName: 'rebounds',
      type: 'number',
      width: 100,
      align: 'left',
      headerAlign: 'left',
      editable: true,
    },
    {
      field: 'blocks',
      headerName: 'blocks',
      type: 'number',
      width: 100,
      align: 'left',
      headerAlign: 'left',
      editable: true,
    },
    {
      field: 'steals',
      headerName: 'steals',
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