import * as React from 'react';
import { Button, Paragraph, Dialog, Portal } from 'react-native-paper';

/**
 * Component for displaying the dialog.
 * @param {bool} show If true show the dialog, if false - hide it.
 * @param {string} title Title of the dialog.
 * @param {string} message Message to display in dialog view.
 * @param {function} hide Method reference for hiding the dialog view.
 * @param {function} confirmBooking Method reference for booking the parking spot.
 * @return {Dialog} Returns styled Dialog for confirming booking the parking place.
 */

const PkDialog = props => {
  return (
    <Portal>
      <Dialog visible={props.show} onDismiss={props.hide}>
        <Dialog.Title>{props.title}</Dialog.Title>
        <Dialog.Content>
          <Paragraph>{props.message}</Paragraph>
        </Dialog.Content>
        <Dialog.Actions>
          <Button onPress={props.hide}>Cancel</Button>
          <Button onPress={props.confirmBooking}>OK</Button>
        </Dialog.Actions>
      </Dialog>
    </Portal>
  );
};

export default PkDialog;
