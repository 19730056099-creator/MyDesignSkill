class ItemStore {
  constructor() {
    this.items = [];
    this.nextId = 1;
  }

  list() {
    return [...this.items];
  }

  create(name) {
    const normalized = String(name || '').trim();
    if (!normalized) throw new Error('name is required');
    const item = { id: this.nextId++, name: normalized };
    this.items.push(item);
    return item;
  }
}

module.exports = { ItemStore };
