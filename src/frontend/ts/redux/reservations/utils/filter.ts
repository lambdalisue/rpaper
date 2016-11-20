import * as moment from 'moment';
import {
  Filter, NoFilter, YearFilter, MonthFilter, DateFilter
} from '../models';


function buildYearFilterParam(filter: YearFilter) {
  const since = moment([filter.year]).startOf('year').startOf('date');
  const until = moment(since).endOf('year').endOf('date');
  return {
    since: since.format(),
    until: until.format(),
  };
}

function buildMonthFilterParam(filter: MonthFilter) {
  const since = moment([
    filter.year,
    filter.month-1
  ]).startOf('month').startOf('date');
  const until = moment(since).endOf('month').endOf('date');
  return {
    since: since.format(),
    until: until.format(),
  };
}

function buildDateFilterParam(filter: DateFilter) {
  const since = moment([
    filter.year,
    filter.month-1,
    filter.date
  ]).startOf('date');
  const until = moment(since).endOf('date');
  return {
    since: since.format(),
    until: until.format(),
  };
}

export function buildFilterParam(filter: Filter) {
  const filterType = getFilterType(filter);
  switch(filterType) {
    case FilterType.NoFilter:
      return {};
    case FilterType.YearFilter:
      return buildYearFilterParam(<YearFilter>filter);
    case FilterType.MonthFilter:
      return buildMonthFilterParam(<MonthFilter>filter);
    case FilterType.DateFilter:
      return buildDateFilterParam(<DateFilter>filter);
  }
}

export enum FilterType {
  NoFilter,
  YearFilter,
  MonthFilter,
  DateFilter,
};

export function getFilterType(filter: Filter): FilterType {
  const hasYear  = !!filter.year;
  const hasMonth = !!filter.month;
  const hasDate  = !!filter.date;
  if (hasYear && hasMonth && hasDate) {
    return FilterType.DateFilter;
  }
  else if (hasYear && hasMonth) {
    return FilterType.MonthFilter;
  }
  else if (hasYear) {
    return FilterType.YearFilter;
  }
  return FilterType.NoFilter;
}
