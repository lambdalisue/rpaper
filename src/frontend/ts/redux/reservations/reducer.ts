import * as moment from 'moment';
import { merge } from 'lodash';
import { handleActions, Action } from 'redux-actions';

import { Thing, Record, RecordError, Filter, State } from './models';
import {
  REQUEST_THING,
  RECEIVE_THING,
  REQUEST_RECORDS,
  RECEIVE_RECORDS,
  REQUEST_RECORD,
  RECEIVE_RECORD,
  RECEIVE_RECORD_ERROR,
  SET_FILTER,
} from './actions';


export const initialState: State = {
  thing: {
    isFetching: false,
    instance: null,
    records: {
      isFetching: false,
      filter: {},
      items: [],
    }
  },
  error: {},
};


type Payload = void | Thing | Record | Record[] | Filter;

const reducer = handleActions<State, Payload>({
  [REQUEST_THING]: (state: State, action: Action<void>): State => {
    return merge({}, state, {
      thing: {
        isFetching: true,
      },
    });
  },

  [RECEIVE_THING]: (state: State, action: Action<Thing>): State => {
    return merge({}, state, {
      thing: {
        isFetching: false,
        instance: action.payload,
      },
    });
  },

  [REQUEST_RECORDS]: (state: State, action: Action<void>): State => {
    return merge({}, state, {
      thing: {
        records: {
          isFetching: true,
        }
      },
    });
  },

  [RECEIVE_RECORDS]: (state: State, action: Action<Record[]>): State => {
    return merge({}, state, {
      thing: {
        records: {
          isFetching: false,
          items: action.payload,
        }
      },
    });
  },

  [REQUEST_RECORD]: (state: State, action: Action<void>): State => {
    return merge({}, state, {
      thing: {
        records: {
          isFetching: true,
        }
      },
    });
  },

  [RECEIVE_RECORD]: (state: State, action: Action<Record>): State => {
    return merge({}, state, {
      thing: {
        records: {
          isFetching: false,
          items: state.thing.records.items.concat([action.payload]),
        }
      },
      error: {
        record: {},
      }
    });
  },

  [RECEIVE_RECORD_ERROR]: (state: State, action: Action<RecordError>): State => {
    return merge({}, state, {
      error: {
        record: action.payload,
      }
    });
  },

  [SET_FILTER]: (state: State, action: Action<Filter>): State => {
    return merge({}, state, {
      thing: {
        records: {
          filter: action.payload,
        }
      },
    });
  },
}, initialState);

export default reducer;
