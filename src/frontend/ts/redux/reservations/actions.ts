import * as moment from 'moment';
import { request } from 'ts/utils/http';
import { Dispatch, ThunkAction } from 'redux';
import { createAction } from 'redux-actions';
import {
  Thing,
  Record, RecordForm, RecordError,
  Filter,
  State,
} from './models';
import { buildFilterParam } from './utils/filter';


export const REQUEST_THING = 'REQUEST_THING';
export const requestThing = createAction<void>(REQUEST_THING);
export const RECEIVE_THING = 'RECEIVE_THING';
export const receiveThing = createAction<Thing>(RECEIVE_THING);

export function fetchThing(param: {pk: string}): ThunkAction<void, {}, {}> {
  return function (dispatch) {
    // Tell that the requesting has started.
    dispatch(requestThing());

    return request(`/api/${param.pk}/`)
      .then(response => response.json())
      .then(json => {
        dispatch(receiveThing(<Thing>json));
      })
      .catch(error => {
        console.error(error);
      });
  };
}


export const REQUEST_RECORDS = 'REQUEST_RECORDS';
export const requestRecords = createAction<void>(REQUEST_RECORDS);
export const RECEIVE_RECORDS = 'RECEIVE_RECORDS';
export const receiveRecords = createAction<Record[]>(RECEIVE_RECORDS);

export function fetchRecords(param: {pk: string, filter: Filter}): ThunkAction<void, {}, {}> {
  return function (dispatch) {
    dispatch(requestRecords());

    const init = {
      params: buildFilterParam(param.filter),
    };
    return request(`/api/${param.pk}/records/`, init)
      .then(response => response.json())
      .then(json => {
        const records = <Record[]>json.map((item) => {
          return Object.assign({}, item, {
            start_at: moment(item.start_at),
            end_at: moment(item.end_at),
          });
        });
        dispatch(receiveRecords(records));
      })
      .catch(error => {
        console.error(error);
      });
  };
}

export const REQUEST_RECORD = 'REQUEST_RECORD';
export const requestRecord = createAction<void>(REQUEST_RECORD);
export const RECEIVE_RECORD = 'RECEIVE_RECORD';
export const receiveRecord = createAction<Record>(RECEIVE_RECORD);
export const RECEIVE_RECORD_ERROR = 'RECEIVE_RECORD_ERROR';
export const receiveRecordError = createAction<RecordError>(RECEIVE_RECORD_ERROR);

export function postRecord(param: {pk: string, form: RecordForm}): ThunkAction<void, {}, {}> {
  return function (dispatch) {
    dispatch(requestRecord());

    const init = {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(param.form),
    };
    console.log(param, init)
    return request(`/api/${param.pk}/records/`, init)
      .then(response => response.json())
      .then(json => {
        const record = Object.assign({}, json, {
          start_at: moment(json.start_at),
          end_at: moment(json.end_at),
        });
        dispatch(receiveRecord(record));
      })
      .catch(error => {
        return error.response.json()
      })
      .then(json => {
        dispatch(receiveRecordError(json));
      })
  };
}


export const SET_FILTER = 'SET_FILTER';
export const setFilter = createAction<Filter>(SET_FILTER);
