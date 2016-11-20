<mdl-input>
  <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">
    <input class="mdl-textfield__input"
      id={ id }
      type={ type }
      autocomplete={ autocomplete }
      disabled={ disabled }
      inputmode={ inputmode }
      max={ max }
      maxlength={ maxlength }
      min={ min }
      minlength={ minlength }
      placeholder={ placeholder }
      readonly={ readonly }
      required={ required }
      spellcheck={ spellcheck }
      step={ step }
    />
    <label class="mdl-textfield__label" for={ id }>{ label }</label>
    <span class="mdl-textfield__error">{ validationMessage }</span>
  </div>

  <script>
    const EXTRA_ATTRIBUTES = [
      'type',
      'autocomplete',
      'disabled',
      'inputmode',
      'max',
      'maxlength',
      'min',
      'minlength',
      'pattern',
      'placeholder',
      'readonly',
      'required',
      'spellcheck',
      'step',
      'value',
    ];

    let getMaterialTextfield = () => {
      return this._field.parentElement.MaterialTextfield;
    };

    this.on('mount', () => {
      this.root.removeAttribute('id');
      this._field = this.root.querySelector('input');
      this._field.addEventListener('invalid', (e) => {
        this.validationMessage = e.target.validationMessage;
        this.update();
        getMaterialTextfield().checkValidity();
      });
      this.validationMessage = this._field.validationMessage;
    });

    this.on('update', () => {
      this.id    = opts.id;
      this.label = opts.label;
      for (let key of EXTRA_ATTRIBUTES) {
        if (key in opts) {
          this[key] = opts[key];
        }
        else {
          this[key] = false;
        }
      }
    });
  </script>
</mdl-input>

