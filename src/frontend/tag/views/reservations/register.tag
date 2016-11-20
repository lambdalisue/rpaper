import 'tag/mdl/mdl-input';

<reservations-register>
  <form onsubmit={ submit }>
    <mdl-input id="name" type="text" label="{ gettext('Name') }"/>
    <mdl-input id="contact" type="text" label="{ gettext('Contact') }"/>
    <mdl-input id="remarks" type="text" label="{ gettext('Remarks') }"/>
    <mdl-input id="start_at" type="datetime" label="{ gettext('Start at') }"/>
    <mdl-input id="end_at" type="datetime" label="{ gettext('End at') }"/>
    <button class="mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect">
      { gettext('Submit') }
    </button>
  </form>

  <script>
    import moment from 'moment';
    import store from 'ts/redux/store';
    import { postRecord } from 'ts/redux/reservations/actions';

    const assignFieldProperty = (obj, name) => {
      Object.defineProperty(obj, name, {
        get() {
          return obj.root.querySelector(`#${name}`);
        }
      });
    }

    const clearCustomValidityOnce = (e) => {
      e.target.setCustomValidity('');
      e.target.removeEventListener(e.type, clearCustomValidityOnce);
    };

    store.subscribe(() => {
      const state = store.getState();
      const error = (state.reservations.error || {}).record || {};
      if (this.error !== error) {
        this.update({
          error: error,
        });
      }
    });

    this.on('update', () => {
      this.state = opts.state;
    });

    this.on('updated', () => {
      this.state = opts.state;
      // Re-assign fields as property while MDL re-write ID attribute
      assignFieldProperty(this, 'name');
      assignFieldProperty(this, 'contact');
      assignFieldProperty(this, 'remarks');
      assignFieldProperty(this, 'start_at');
      assignFieldProperty(this, 'end_at');
      // Assign custom validities
      for(let key in this.error) {
        console.debug(key, this.error[key]);
        this[key].setCustomValidity(this.error[key][0]);
        this[key].addEventListener('input', clearCustomValidityOnce);
      }
    });

    this.submit = () => {
      store.dispatch(postRecord({
        pk: this.state.thing.instance.pk,
        form: {
          name: this.name.value,
          contact: this.contact.value,
          remarks: this.remarks.value,
          start_at: this.start_at.value,
          end_at: this.end_at.value,
        }
      }));
      return false;
    }
  </script>
</reservations-register>
