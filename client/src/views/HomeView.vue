<template>
  <main>
    <h1 class="mb-4">Каталог книг</h1>
    <div class="list-group">
      <RouterLink to="/authors" class="list-group-item list-group-item-action">Авторы</RouterLink>
      <RouterLink to="/genres" class="list-group-item list-group-item-action">Жанры</RouterLink>
      <RouterLink to="/series" class="list-group-item list-group-item-action">Серии</RouterLink>
      <RouterLink to="/publishers" class="list-group-item list-group-item-action">Издательства</RouterLink>
      <RouterLink to="/books" class="list-group-item list-group-item-action">Книги</RouterLink>
    </div>
  </main>
</template>
