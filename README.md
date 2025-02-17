пример POST запроса, создание нового заказа:
{
  "status": "waiting",
  "table_number": 44,
  "items": [
    {
      "item": 1, 
      "quantity": 2
    },
    {
      "item": 2,
      "quantity": 3
    }
  ]
}

Пример PUT запроса, изменени заказа по id:
{
 "table_number": 44,
  "status": "paid",
  "items": [
    {
      "item": 1,
      "quantity": 5
    },
    {
      "item": 3,
      "quantity": 2
    }
  ]
}