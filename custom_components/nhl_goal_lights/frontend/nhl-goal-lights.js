class NHLPanel extends HTMLElement {
  connectedCallback() {
    this.innerHTML = `
      <ha-card>
        <h1>NHL Goal Lights</h1>
        <timeline-editor></timeline-editor>
      </ha-card>
    `;
  }
}

customElements.define("nhl-goal-lights", NHLPanel);