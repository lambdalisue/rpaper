import * as moment from 'moment';

export interface User {
  username: string;
  email: string;
}

export interface Filter {
  year?: number;
  month?: number;
  date?: number;
}

export interface NoFilter extends Filter {
  year: null;
  month: null;
  date: null;
}

export interface YearFilter extends Filter {
  year: number;
  month: null;
  date: null;
}

export interface MonthFilter extends Filter {
  year: number;
  month: number;
  date: null;
}

export interface DateFilter extends Filter {
  year: number;
  month: number;
  date: number;
}

export interface Thing {
  pk: string;
  name: string;
  remarks: string;
  thumbnail?: string;
  owner: User;
}

export interface Record {
  pk: string;
  name: string;
  contact: string;
  remarks: string;
  start_at: moment.Moment;
  end_at: moment.Moment;
}

export interface RecordForm {
  name: string;
  contact: string;
  remarks: string;
  start_at: string;
  end_at: string;
}

export interface RecordError {
  name?: string[];
  contact?: string[];
  remarks?: string[];
  start_at?: string[];
  end_at?: string[];
}


export interface State {
  thing: {
    isFetching: boolean;
    instance: Thing;
    records: {
      isFetching: boolean;
      filter: Filter;
      items: Record[];
    };
  };
  error: {
    record?: RecordError;
  }
}
