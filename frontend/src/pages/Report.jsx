import React, { useState } from 'react';
import TeamDropdown from '../components/TeamDropdown';
import WinLossRecord from '../components/WinLossRecord';
import TeamPastGames from '../components/TeamPastGames';
import TeamRoster from '../components/TeamRoster';
import TeamStatLeaders from '../components/TeamStatLeaders';

export default function Report() {
  const [selectedTeam, setSelectedTeam] = useState(1);

  return (
    <div>
      <h2>Report</h2>
      <h3>Select Team</h3>
      <TeamDropdown selectedTeam={selectedTeam} setSelectedTeam={setSelectedTeam} />
      <WinLossRecord selectedTeam={selectedTeam} />

      <div style={{ display: 'flex', justifyContent: 'flex-start' }}>
        <div style={{ marginRight: '10px' }}>
          <h3>Roster</h3>
          <TeamRoster selectedTeam={selectedTeam} />
        </div>

        <div style={{ marginRight: '10px' }}>
          <h3>Leaders</h3>
          <TeamStatLeaders selectedTeam={selectedTeam} />
        </div>

        <div>
          <h3>Past Games</h3>
          <TeamPastGames selectedTeam={selectedTeam} />
        </div>
      </div>

    </div>
  );
}
