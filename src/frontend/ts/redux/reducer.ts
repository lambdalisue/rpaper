import { combineReducers } from 'redux';
import reservations from './reservations';


const rootReducer = combineReducers({
  reservations,
});

export default rootReducer;
