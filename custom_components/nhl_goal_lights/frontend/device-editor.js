class DeviceEditor extends HTMLElement {
  connectedCallback() {
    this.innerHTML = `
      <ha-card>
        <h2>Device Config</h2>
        <input id="device" placeholder="light.wled_tv"/>
        <button id="save">Save</button>
      </ha-card>
    `;

    this.querySelector("#save").onclick = () => {
      fetch("/api/nhl_goal_lights/device", {
        method: "POST",
        body: JSON.stringify({
          device: this.querySelector("#device").value
        })
      });
    };
  }
}

customElements.define("device-editor", DeviceEditor);