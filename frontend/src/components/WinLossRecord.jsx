import React, { useState, useEffect } from 'react';
import axios from 'axios';

export default function WinLossRecord({selectedTeam}) {
  const [record, setRecord] = useState({ wins: 0, losses: 0 });

  // Function to fetch win loss record from API
  const fetchWinLossRecord = async () => {
    try {
      const response = await axios.get('/report/get_record', {
        params: {
          team_id: String(selectedTeam)
        }
      });
      setRecord(response.data);
    } catch (error) {
      console.error("Error fetching win-loss record: ", error);
    }
  };

  useEffect(() => {
    fetchWinLossRecord()
  }, [selectedTeam]);

  return (
    <div>
      <p><b>Win-Loss Record:</b> {record.wins}-{record.losses}</p>
    </div>
  );
};
