import React, { useState, useEffect } from 'react';
import { Snackbar } from 'react-native-paper';

/**
 * Component for displaying Snackbar - a small container with text at the bottom of the screen.
 * @param {bool} visible If true than show Snackbar in other cases - do not show it
 * @param {string} text Text string for displaying the message in the Snackbar
 * @param {number} seconds For how many seconds display the Snackbar 
 * @returns {PkSnackbar} Returns component for displaying the message at the bottom of the screen for certain amount of seconds.
 */

const PkSnackbar = props => {
  const [isVisible, setVisibility] = useState(false);

  const showSnackbar = () => setVisibility(true);
  const hideSnackbar = () => setVisibility(false);
  
  const showSnackbarForSeconds = () => {
    const secondsToShow = props.seconds * 1000; 
    showSnackbar();
    setTimeout(() => hideSnackbar(), secondsToShow);
  };

  useEffect(() => {
    if(!props.visible){
      return;
    }
    showSnackbarForSeconds();
  }, [props.visible]);

  return (
    <Snackbar visible={isVisible}>
      {props.text}
    </Snackbar>
  );
};

export default PkSnackbar;
