export function exposeInstanceAttributes(namespace, instance) {
  for (let key in instance) {
    if (instance.hasOwnProperty(key)) {
      namespace[key] = instance[key];
    }
  }
}
