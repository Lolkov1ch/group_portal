````markdown
# Інструкція Як працювати з Git (GitFlow)

1. Перейти на `develop` та оновити його:

   ```bash
   git checkout develop
   git pull origin develop
   ```

2. Подивитися свій таск у Trello.
   Назва гілки = ID таска, наприклад: `FOR-2`, `GL-3`, `AUTH-1` тощо.

3. Створити гілку від `develop`:

   ```bash
   git checkout -b FOR-2
   ```

4. Зробити зміни в коді, запустити проєкт і перевірити, що все працює.

5. Додати файли та зробити коміт:

   ```bash
   git add .
   git commit -m "FOR-2 - коротко-що-робиш"
   ```

6. Відправити гілку на GitHub:

   ```bash
   git push origin FOR-2
   ```

---

## 3. Як зробити Pull Request

1. На GitHub створити **Pull Request** з гілки `FOR-2` → `develop`.
2. У **Title** написати: `FOR-2: короткий опис`.
3. У **Description**:

   * посилання на картку в Trello;
   * коротко, що зроблено.
4. У Pull Request призначити:

   * **Reviewers:** керівника проєкту (**Доцин Андрій(Lolkov1ch)** або **(Angellllna)**,
   * **Assignees:** себе.
5. Дочекатися рев’ю й виправити зауваження, якщо будуть.

```
