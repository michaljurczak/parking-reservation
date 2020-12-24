import React from 'react';
import { ActivityIndicator } from 'react-native-paper'

import CenterView from './styled/CenterView';

/**
 * Comoponent showing loading animation.
 * @param {bool} animating If true - show loading animation, if false - hide it.
 * @returns {Loading} Returns component with loading animation.  
 */

const Loading = props => {
  return (
    <CenterView>
      <ActivityIndicator
        animating={props.animating}
        size="large"
      />
    </CenterView>
  );
};

export default Loading;
