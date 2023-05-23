const usedIds = new Set();

function getUniqueId() {
  let id = 0;
  while (usedIds.has(id)) {
    id++;
  }
  usedIds.add(id);
  return id;
}

function freeId(id) {
  usedIds.delete(id);
}

module.exports = {getUniqueId, freeId};
