### Как использовать скрипт
1. Список транзакций и для стейкинга, и для leave_all должен иметь следующий формат:

    ```
    {private_key},{amount}/{private_key},{amount}/{private_key},{amount}
    ```

    То есть, для каждой транзакции указывается приватник (`private_key`) и сумма транзакции (`amount`) через запятую, а транзакции отделены между собой слешем (/). Пример: 
    ```
    e240cda9bccef7fb65fa307f3a783b13c801305c9e7cad551c3b604ae353c6b9,952380952380952380947/e240cda9bccef7fb65fa307f3a783b13c801305c9e7cad551c3b604ae353c6b9,1074285714285714285708/e240cda9bccef7fb65fa307f3a783b13c801305c9e7cad551c3b604ae353c6b9,1428571428571428571421
    ```
2. Скрипт запускается командой `python rubic_test_staking_script.py`, далее идут аргументы через пробел:
   * для стейкинга: просто список транзакций, как в пункте 1, `amount` без домножения на 10^18
   * для can receive: `can_receive {amount}`. Пример:
   `python rubic_test_staking_script.py can_receive 952380952380952380947`
   * для leave по одной транзакции: `leave {private_key} {amount}`. Пример: `python rubic_test_staking_script.py e240cda9bccef7fb65fa307f3a783b13c801305c9e7cad551c3b604ae353c6b9 1428571428571428571421`
   * для массового leave: `leave_all {list}`, где `list` — список транзакций, как в пункте 1, `amount` помноженный на 10^18
   * для transfer: `transfer {token_contract} {user_priv_from} {list}`, где `list` — список транзакций, как в пункте 1, `amount` без домножения на 10^18
   * для отправки нативной валюты: `crypto_send {user_priv_from} {list}`
3. Результат работы скрипта:
   * в случае стейкинга: после каждой транзакции будет возвращаться инфа в виде `({private_key}, {transaction_hash}, {approve_status}, {minted_xrbc})`. В случае ошибки с транзакцией (какой-то call не прошел) может вернуться не вся инфа. В конце работы скрипта вернется список транзакций, как в пункте 1, который можно потом будет скормить `leave_all`.
   * в случае can receive: число в 10^18
   * в случае leave по одной транзакции: хеш транзакции
   * в случае массового leave: после каждой транзакции будет возвращаться хеш транзакции
   * в случае transfer: после каждой транзакции будет возвращаться хеш транзакции
   * в случае отправки нативной валюты: после каждой транзакции будет возвращаться хеш транзакции