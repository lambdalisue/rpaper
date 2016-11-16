<reservation draggable="true">
  <span class="name">{ name }</span>

  <span class="contact">
    <i class="material-icons">call</i>
    { contact }
  </span>
  <span class="remarks">{ remarks }</span>

  <div class="duration">
    <time class="start_at" datetime="{ start_at }">
      { start_at.format("kk:mm") }
    </time>
    <time class="end_at" datetime="{ end_at }">
      { end_at.format("kk:mm") }
    </time>
  </div>

  <style>
  reservation {
    position: relative;
    display: block;
    margin: 10px;
    margin-left: 50px;
    padding-left: calc(40px + 2em);
    width: 100px;
    height: 50px;
    border-radius: 10px;
    background-color: #808f85;
    color: #fff;
    cursor: pointer;
  }
  .contact {
    position: absolute;
    bottom: 0.1em;
    right: 0.1em;
  }
  .duration {
    position: absolute;
    display: flex;
    flex-direction: column;
    justify-content: center;
    top: -0px;
    left: -20px;
    width: 40px;
    height: 40px;
    border: 5px solid #808f85;
    border-radius: 50%;
    background-color: #91c499;
    font-size: xx-small;
    z-index: 1;
  }
  .duration time {
    display: block;
    text-align: center;
    font-weight: bold;
    line-height: 1.1em;
  }
  .duration .start_at:after {
    display: block;
    content: "~";
    transform: rotate(90deg);
  }
  </style>

  <script>
  let self = this;
  const url = `/api/instruments/${opts.instrument_pk}/reservations/${opts.pk}/`;

  fetch(url)
    .then((data) => {
      return data.json();
    })
    .then((json) => {
      this.name = json.name;
      this.contact = json.contact;
      this.remarks = json.remarks;
      this.start_at = moment(json.start_at);
      this.end_at = moment(json.end_at);
      this.update();
    });

  this.on('mount', () => {
    this.root.addEventListener('dragstart', (event) => {
      this.root.style.opacity = '0.4';
    }, false);
  });

  </script>
</reservation>
