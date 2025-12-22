Title: API docs — ib_async 2.1.0 documentation

----------------------------------------------------------------------------------------------------

High-level interface to Interactive Brokers.

_class_ ib_async.ib.StartupFetch(_value_, _names=<not given>_, _*values_, _module=None_, _qualname=None_, _type=None_, _start=1_, _boundary=None_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#StartupFetch)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.StartupFetch "Link to this definition")POSITIONS _=1_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.StartupFetch.POSITIONS "Link to this definition")ORDERS_OPEN _=2_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.StartupFetch.ORDERS_OPEN "Link to this definition")ORDERS_COMPLETE _=4_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.StartupFetch.ORDERS_COMPLETE "Link to this definition")ACCOUNT_UPDATES _=8_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.StartupFetch.ACCOUNT_UPDATES "Link to this definition")SUB_ACCOUNT_UPDATES _=16_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.StartupFetch.SUB_ACCOUNT_UPDATES "Link to this definition")EXECUTIONS _=32_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.StartupFetch.EXECUTIONS "Link to this definition")_class_ ib_async.ib.IB(_defaults=IBDefaults(emptyPrice=-1,emptySize=0,unset=nan,timezone=datetime.timezone.utc)_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB "Link to this definition")
Provides both a blocking and an asynchronous interface to the IB API, using asyncio networking and event loop.

The IB class offers direct access to the current state, such as orders, executions, positions, tickers etc. This state is automatically kept in sync with the TWS/IBG application.

This class has most request methods of EClient, with the same names and parameters (except for the reqId parameter which is not needed anymore). Request methods that return a result come in two versions:

*   Blocking: Will block until complete and return the result. The current state will be kept updated while the request is ongoing;

*   Asynchronous: All methods that have the “Async” postfix. Implemented as coroutines or methods that return a Future and intended for advanced users.

**The One Rule:**

While some of the request methods are blocking from the perspective of the user, the framework will still keep spinning in the background and handle all messages received from TWS/IBG. It is important to not block the framework from doing its work. If, for example, the user code spends much time in a calculation, or uses time.sleep() with a long delay, the framework will stop spinning, messages accumulate and things may go awry.

The one rule when working with the IB class is therefore that

**user code may not block for too long**.

To be clear, the IB request methods are okay to use and do not count towards the user operation time, no matter how long the request takes to finish.

So what is “too long”? That depends on the situation. If, for example, the timestamp of tick data is to remain accurate within a millisecond, then the user code must not spend longer than a millisecond. If, on the other extreme, there is very little incoming data and there is no desire for accurate timestamps, then the user code can block for hours.

If a user operation takes a long time then it can be farmed out to a different process. Alternatively the operation can be made such that it periodically calls IB.sleep(0); This will let the framework handle any pending work and return when finished. The operation should be aware that the current state may have been updated during the sleep(0) call.

For introducing a delay, never use time.sleep() but use [`sleep()`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.sleep "ib_async.ib.IB.sleep") instead.

Parameters:
*   **RequestTimeout** ([_float_](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")) – Timeout (in seconds) to wait for a blocking request to finish before raising `asyncio.TimeoutError`. The default value of 0 will wait indefinitely. Note: This timeout is not used for the `*Async` methods.

*   **RaiseRequestErrors** ([_bool_](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")) –

Specifies the behaviour when certain API requests fail:

    *   [`False`](https://docs.python.org/3/library/constants.html#False "(in Python v3.14)"): Silently return an empty result;

    *   [`True`](https://docs.python.org/3/library/constants.html#True "(in Python v3.14)"): Raise a [`RequestError`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.wrapper.RequestError "ib_async.wrapper.RequestError").

*   **MaxSyncedSubAccounts** ([_int_](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) – Do not use sub-account updates if the number of sub-accounts exceeds this number (50 by default).

*   **TimezoneTWS** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – Specifies what timezone TWS (or gateway) is using. The default is to assume local system timezone.

Events:
*   `connectedEvent` (): Is emitted after connecting and synchronzing with TWS/gateway.

*   `disconnectedEvent` (): Is emitted after disconnecting from TWS/gateway.

*   `updateEvent` (): Is emitted after a network packet has been handled.

*   `pendingTickersEvent` (tickers: Set[[`Ticker`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker "ib_async.ticker.Ticker")]): Emits the set of tickers that have been updated during the last update and for which there are new ticks, tickByTicks or domTicks.

*   `barUpdateEvent` (bars: [`BarDataList`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.BarDataList "ib_async.objects.BarDataList"), hasNewBar: bool): Emits the bar list that has been updated in real time. If a new bar has been added then hasNewBar is True, when the last bar has changed it is False.

*   `newOrderEvent` (trade: [`Trade`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Trade "ib_async.order.Trade")): Emits a newly placed trade.

*   `orderModifyEvent` (trade: [`Trade`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Trade "ib_async.order.Trade")): Emits when order is modified.

*   `cancelOrderEvent` (trade: [`Trade`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Trade "ib_async.order.Trade")): Emits a trade directly after requesting for it to be cancelled.

*   `openOrderEvent` (trade: [`Trade`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Trade "ib_async.order.Trade")): Emits the trade with open order.

*   `orderStatusEvent` (trade: [`Trade`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Trade "ib_async.order.Trade")): Emits the changed order status of the ongoing trade.

*   `execDetailsEvent` (trade: [`Trade`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Trade "ib_async.order.Trade"), fill: [`Fill`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.Fill "ib_async.objects.Fill")): Emits the fill together with the ongoing trade it belongs to.

*   `commissionReportEvent` (trade: [`Trade`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Trade "ib_async.order.Trade"), fill: [`Fill`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.Fill "ib_async.objects.Fill"), report: [`CommissionReport`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.CommissionReport "ib_async.objects.CommissionReport")): The commission report is emitted after the fill that it belongs to.

*   `updatePortfolioEvent` (item: [`PortfolioItem`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.PortfolioItem "ib_async.objects.PortfolioItem")): A portfolio item has changed.

*   `positionEvent` (position: [`Position`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.Position "ib_async.objects.Position")): A position has changed.

*   `accountValueEvent` (value: [`AccountValue`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.AccountValue "ib_async.objects.AccountValue")): An account value has changed.

*   `accountSummaryEvent` (value: [`AccountValue`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.AccountValue "ib_async.objects.AccountValue")): An account value has changed.

*   `pnlEvent` (entry: [`PnL`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.PnL "ib_async.objects.PnL")): A profit- and loss entry is updated.

*   `pnlSingleEvent` (entry: [`PnLSingle`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.PnLSingle "ib_async.objects.PnLSingle")): A profit- and loss entry for a single position is updated.

*   `tickNewsEvent` (news: [`NewsTick`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.NewsTick "ib_async.objects.NewsTick")): Emit a new news headline.

*   `newsBulletinEvent` (bulletin: [`NewsBulletin`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.NewsBulletin "ib_async.objects.NewsBulletin")): Emit a new news bulletin.

*   `scannerDataEvent` (data: [`ScanDataList`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.ScanDataList "ib_async.objects.ScanDataList")): Emit data from a scanner subscription.

*   `wshMetaEvent` (dataJson: str): Emit WSH metadata.

*   `wshEvent` (dataJson: str): Emit WSH event data (such as earnings dates, dividend dates, options expiration dates, splits, spinoffs and conferences).

*   `errorEvent` (reqId: int, errorCode: int, errorString: str, contract: [`Contract`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Contract "ib_async.contract.Contract")): Emits the reqId/orderId and TWS error code and string (see [https://interactivebrokers.github.io/tws-api/message_codes.html](https://interactivebrokers.github.io/tws-api/message_codes.html)) together with the contract the error applies to (or None if no contract applies).

*   `timeoutEvent` (idlePeriod: float): Is emitted if no data is received for longer than the timeout period specified with [`setTimeout()`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.setTimeout "ib_async.ib.IB.setTimeout"). The value emitted is the period in seconds since the last update.

Note that it is not advisable to place new requests inside an event handler as it may lead to too much recursion.

events _=('connectedEvent','disconnectedEvent','updateEvent','pendingTickersEvent','barUpdateEvent','newOrderEvent','orderModifyEvent','cancelOrderEvent','openOrderEvent','orderStatusEvent','execDetailsEvent','commissionReportEvent','updatePortfolioEvent','positionEvent','accountValueEvent','accountSummaryEvent','pnlEvent','pnlSingleEvent','scannerDataEvent','tickNewsEvent','newsBulletinEvent','wshMetaEvent','wshEvent','errorEvent','timeoutEvent')_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.events "Link to this definition")RequestTimeout _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.RequestTimeout "Link to this definition")RaiseRequestErrors _:[`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")_ _=False_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.RaiseRequestErrors "Link to this definition")MaxSyncedSubAccounts _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=50_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.MaxSyncedSubAccounts "Link to this definition")TimezoneTWS _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.TimezoneTWS "Link to this definition")connect(_host='127.0.0.1'_, _port=7497_, _clientId=1_, _timeout=4_, _readonly=False_, _account=''_, _raiseSyncErrors=False_, _fetchFields=<StartupFetch.POSITIONS|ORDERS\_OPEN|ORDERS\_COMPLETE|ACCOUNT\_UPDATES|SUB\_ACCOUNT\_UPDATES|EXECUTIONS:63>_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.connect)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.connect "Link to this definition")
Connect to a running TWS or IB gateway application. After the connection is made the client is fully synchronized and ready to serve requests.

This method is blocking.

Parameters:
*   **host** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – Host name or IP address.

*   **port** ([`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) – Port number.

*   **clientId** ([`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) – ID number to use for this client; must be unique per connection. Setting clientId=0 will automatically merge manual TWS trading with this client.

*   **timeout** ([`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")) – If establishing the connection takes longer than `timeout` seconds then the `asyncio.TimeoutError` exception is raised. Set to 0 to disable timeout.

*   **readonly** ([`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")) – Set to `True` when API is in read-only mode.

*   **account** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – Main account to receive updates for.

*   **raiseSyncErrors** ([`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")) –

When `True` this will cause an initial
sync request error to raise a ConnectionError`. When `False` the error will only be logged at error level.

fetchFields: By default, all account data is loaded and cached
when a new connection is made. You can optionally disable all or some of the account attribute fetching during a connection using the StartupFetch field flags. See `StartupFetch` in `ib.py` for member details. There is also StartupFetchNONE and StartupFetchALL as shorthand. Individual flag field members can be added or removed to the `fetchFields` parameter as needed.

disconnect()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.disconnect)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.disconnect "Link to this definition")
Disconnect from a TWS or IB gateway application. This will clear all session state.

Return type:
[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [`None`](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")

isConnected()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.isConnected)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.isConnected "Link to this definition")
Is there an API connection to TWS or IB gateway?

Return type:
[`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")

_static_ run(_*_, _timeout=None_)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.run "Link to this definition")
By default run the event loop forever.

When awaitables (like Tasks, Futures or coroutines) are given then run the event loop until each has completed and return their results.

An optional timeout (in seconds) can be given that will raise asyncio.TimeoutError if the awaitables are not ready within the timeout period.

_static_ schedule(_callback_, _*args_)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.schedule "Link to this definition")
Schedule the callback to be run at the given time with the given arguments. This will return the Event Handle.

Parameters:
*   **time** ([`time`](https://docs.python.org/3/library/datetime.html#datetime.time "(in Python v3.14)") | [`datetime`](https://docs.python.org/3/library/datetime.html#datetime.datetime "(in Python v3.14)")) – Time to run callback. If given as [`datetime.time`](https://docs.python.org/3/library/datetime.html#datetime.time "(in Python v3.14)") then use today as date.

*   **callback** ([`Callable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Callable "(in Python v3.14)")) – Callable scheduled to run.

*   **args** – Arguments for to call callback with.

_static_ sleep()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.sleep "Link to this definition")
Wait for the given amount of seconds while everything still keeps processing in the background. Never use time.sleep().

Parameters:
**secs** ([_float_](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")) – Time in seconds to wait.

Return type:
[`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")

_static_ timeRange(_end_, _step_)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.timeRange "Link to this definition")
Iterator that waits periodically until certain time points are reached while yielding those time points.

Parameters:
*   **start** ([`time`](https://docs.python.org/3/library/datetime.html#datetime.time "(in Python v3.14)") | [`datetime`](https://docs.python.org/3/library/datetime.html#datetime.datetime "(in Python v3.14)")) – Start time, can be specified as datetime.datetime, or as datetime.time in which case today is used as the date

*   **end** ([`time`](https://docs.python.org/3/library/datetime.html#datetime.time "(in Python v3.14)") | [`datetime`](https://docs.python.org/3/library/datetime.html#datetime.datetime "(in Python v3.14)")) – End time, can be specified as datetime.datetime, or as datetime.time in which case today is used as the date

*   **step** ([_float_](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")) – The number of seconds of each period

Return type:
[`Iterator`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Iterator "(in Python v3.14)")[[`datetime`](https://docs.python.org/3/library/datetime.html#datetime.datetime "(in Python v3.14)")]

_static_ timeRangeAsync(_end_, _step_)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.timeRangeAsync "Link to this definition")
Async version of [`timeRange()`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.timeRange "ib_async.ib.IB.timeRange").

Return type:
[`AsyncIterator`](https://docs.python.org/3/library/collections.abc.html#collections.abc.AsyncIterator "(in Python v3.14)")[[`datetime`](https://docs.python.org/3/library/datetime.html#datetime.datetime "(in Python v3.14)")]

_static_ waitUntil()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.waitUntil "Link to this definition")
Wait until the given time t is reached.

Parameters:
**t** ([`time`](https://docs.python.org/3/library/datetime.html#datetime.time "(in Python v3.14)") | [`datetime`](https://docs.python.org/3/library/datetime.html#datetime.datetime "(in Python v3.14)")) – The time t can be specified as datetime.datetime, or as datetime.time in which case today is used as the date.

Return type:
[`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")

waitOnUpdate(_timeout=0_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.waitOnUpdate)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.waitOnUpdate "Link to this definition")
Wait on any new update to arrive from the network.

Parameters:
**timeout** ([`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")) – Maximum time in seconds to wait. If 0 then no timeout is used.

Note

A loop with `waitOnUpdate` should not be used to harvest tick data from tickers, since some ticks can go missing. This happens when multiple updates occur almost simultaneously; The ticks from the first update are then cleared. Use events instead to prevent this.

Return type:
[`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")

Returns:
`True` if not timed-out, `False` otherwise.

loopUntil(_condition=None_, _timeout=0_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.loopUntil)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.loopUntil "Link to this definition")
Iterate until condition is met, with optional timeout in seconds. The yielded value is that of the condition or False when timed out.

Parameters:
*   **condition** – Predicate function that is tested after every network

*   **update.**

*   **timeout** ([`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")) – Maximum time in seconds to wait. If 0 then no timeout is used.

Return type:
[`Iterator`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Iterator "(in Python v3.14)")[[`object`](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)")]

setTimeout(_timeout=60_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.setTimeout)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.setTimeout "Link to this definition")
Set a timeout for receiving messages from TWS/IBG, emitting `timeoutEvent` if there is no incoming data for too long.

The timeout fires once per connected session but can be set again after firing or after a reconnect.

Parameters:
**timeout** ([`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")) – Timeout in seconds.

managedAccounts()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.managedAccounts)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.managedAccounts "Link to this definition")
List of account names.

Return type:
[`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")]

accountValues(_account=''_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.accountValues)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.accountValues "Link to this definition")
List of account values for the given account, or of all accounts if account is left blank.

Parameters:
**account** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – If specified, filter for this account name.

Return type:
[`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`AccountValue`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.AccountValue "ib_async.objects.AccountValue")]

accountSummary(_account=''_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.accountSummary)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.accountSummary "Link to this definition")
List of account values for the given account, or of all accounts if account is left blank.

This method is blocking on first run, non-blocking after that.

Parameters:
**account** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – If specified, filter for this account name.

Return type:
[`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`AccountValue`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.AccountValue "ib_async.objects.AccountValue")]

portfolio(_account=''_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.portfolio)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.portfolio "Link to this definition")
List of portfolio items for the given account, or of all retrieved portfolio items if account is left blank.

Parameters:
**account** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – If specified, filter for this account name.

Return type:
[`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`PortfolioItem`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.PortfolioItem "ib_async.objects.PortfolioItem")]

positions(_account=''_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.positions)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.positions "Link to this definition")
List of positions for the given account, or of all accounts if account is left blank.

Parameters:
**account** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – If specified, filter for this account name.

Return type:
[`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`Position`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.Position "ib_async.objects.Position")]

pnl(_account=''_, _modelCode=''_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.pnl)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.pnl "Link to this definition")
List of subscribed [`PnL`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.PnL "ib_async.objects.PnL") objects (profit and loss), optionally filtered by account and/or modelCode.

The [`PnL`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.PnL "ib_async.objects.PnL") objects are kept live updated.

Parameters:
*   **account** – If specified, filter for this account name.

*   **modelCode** – If specified, filter for this account model.

Return type:
[`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`PnL`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.PnL "ib_async.objects.PnL")]

pnlSingle(_account=''_, _modelCode=''_, _conId=0_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.pnlSingle)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.pnlSingle "Link to this definition")
List of subscribed [`PnLSingle`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.PnLSingle "ib_async.objects.PnLSingle") objects (profit and loss for single positions).

The [`PnLSingle`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.PnLSingle "ib_async.objects.PnLSingle") objects are kept live updated.

Parameters:
*   **account** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – If specified, filter for this account name.

*   **modelCode** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – If specified, filter for this account model.

*   **conId** ([`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) – If specified, filter for this contract ID.

Return type:
[`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`PnLSingle`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.PnLSingle "ib_async.objects.PnLSingle")]

trades()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.trades)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.trades "Link to this definition")
List of all order trades from this session.

Return type:
[`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`Trade`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Trade "ib_async.order.Trade")]

openTrades()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.openTrades)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.openTrades "Link to this definition")
List of all open order trades.

Return type:
[`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`Trade`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Trade "ib_async.order.Trade")]

orders()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.orders)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.orders "Link to this definition")
List of all orders from this session.

Return type:
[`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`Order`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order "ib_async.order.Order")]

openOrders()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.openOrders)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.openOrders "Link to this definition")
List of all open orders.

Return type:
[`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`Order`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order "ib_async.order.Order")]

fills()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.fills)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.fills "Link to this definition")
List of all fills from this session.

Return type:
[`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`Fill`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.Fill "ib_async.objects.Fill")]

executions()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.executions)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.executions "Link to this definition")
List of all executions from this session.

Return type:
[`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`Execution`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.Execution "ib_async.objects.Execution")]

ticker(_contract_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.ticker)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.ticker "Link to this definition")
Get ticker of the given contract. It must have been requested before with reqMktData with the same contract object. The ticker may not be ready yet if called directly after [`reqMktData()`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.reqMktData "ib_async.ib.IB.reqMktData").

Parameters:
**contract** ([`Contract`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Contract "ib_async.contract.Contract")) – Contract to get ticker for.

Return type:
[`Ticker`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker "ib_async.ticker.Ticker") | [`None`](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")

tickers()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.tickers)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.tickers "Link to this definition")
Get a list of all tickers.

Return type:
[`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`Ticker`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker "ib_async.ticker.Ticker")]

pendingTickers()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.pendingTickers)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.pendingTickers "Link to this definition")
Get a list of all tickers that have pending ticks or domTicks.

Return type:
[`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`Ticker`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker "ib_async.ticker.Ticker")]

realtimeBars()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.realtimeBars)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.realtimeBars "Link to this definition")
Get a list of all live updated bars. These can be 5 second realtime bars or live updated historical bars.

Return type:
[`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`BarDataList`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.BarDataList "ib_async.objects.BarDataList") | [`RealTimeBarList`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.RealTimeBarList "ib_async.objects.RealTimeBarList")]

newsTicks()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.newsTicks)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.newsTicks "Link to this definition")
List of ticks with headline news. The article itself can be retrieved with [`reqNewsArticle()`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.reqNewsArticle "ib_async.ib.IB.reqNewsArticle").

Return type:
[`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`NewsTick`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.NewsTick "ib_async.objects.NewsTick")]

newsBulletins()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.newsBulletins)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.newsBulletins "Link to this definition")
List of IB news bulletins.

Return type:
[`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`NewsBulletin`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.NewsBulletin "ib_async.objects.NewsBulletin")]

reqTickers(_*contracts_, _regulatorySnapshot=False_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.reqTickers)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.reqTickers "Link to this definition")
Request and return a list of snapshot tickers. The list is returned when all tickers are ready.

This method is blocking.

Parameters:
*   **contracts** ([`Contract`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Contract "ib_async.contract.Contract")) – Contracts to get tickers for.

*   **regulatorySnapshot** ([`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")) – Request NBBO snapshots (may incur a fee).

Return type:
[`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`Ticker`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker "ib_async.ticker.Ticker")]

qualifyContracts(_*contracts_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.qualifyContracts)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.qualifyContracts "Link to this definition")
Fully qualify the given contracts in-place. This will fill in the missing fields in the contract, especially the conId.

Returns a list of contracts that have been successfully qualified.

This method is blocking.

Parameters:
**contracts** ([`Contract`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Contract "ib_async.contract.Contract")) – Contracts to qualify.

Return type:
[`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`Contract`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Contract "ib_async.contract.Contract")]

bracketOrder(_action_, _quantity_, _limitPrice_, _takeProfitPrice_, _stopLossPrice_, _**kwargs_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.bracketOrder)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.bracketOrder "Link to this definition")
Create a limit order that is bracketed by a take-profit order and a stop-loss order. Submit the bracket like:

for o in bracket:
    ib.placeOrder(contract, o)

[https://interactivebrokers.github.io/tws-api/bracket_order.html](https://interactivebrokers.github.io/tws-api/bracket_order.html)

Parameters:
*   **action** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – ‘BUY’ or ‘SELL’.

*   **quantity** ([`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")) – Size of order.

*   **limitPrice** ([`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")) – Limit price of entry order.

*   **takeProfitPrice** ([`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")) – Limit price of profit order.

*   **stopLossPrice** ([`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")) – Stop price of loss order.

Return type:
[`BracketOrder`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.BracketOrder "ib_async.order.BracketOrder")

_static_ oneCancelsAll(_orders_, _ocaGroup_, _ocaType_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.oneCancelsAll)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.oneCancelsAll "Link to this definition")
Place the trades in the same One Cancels All (OCA) group.

[https://interactivebrokers.github.io/tws-api/oca.html](https://interactivebrokers.github.io/tws-api/oca.html)

Parameters:
**orders** ([`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`Order`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order "ib_async.order.Order")]) – The orders that are to be placed together.

Return type:
[`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`Order`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order "ib_async.order.Order")]

whatIfOrder(_contract_, _order_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.whatIfOrder)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.whatIfOrder "Link to this definition")
Retrieve commission and margin impact without actually placing the order. The given order will not be modified in any way.

This method is blocking.

Parameters:
*   **contract** ([`Contract`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Contract "ib_async.contract.Contract")) – Contract to test.

*   **order** ([`Order`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order "ib_async.order.Order")) – Order to test.

Return type:
[`OrderState`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderState "ib_async.order.OrderState")

placeOrder(_contract_, _order_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.placeOrder)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.placeOrder "Link to this definition")
Place a new order or modify an existing order. Returns a Trade that is kept live updated with status changes, fills, etc.

Parameters:
*   **contract** ([`Contract`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Contract "ib_async.contract.Contract")) – Contract to use for order.

*   **order** ([`Order`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order "ib_async.order.Order")) – The order to be placed.

Return type:
[`Trade`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Trade "ib_async.order.Trade")

cancelOrder(_order_, _manualCancelOrderTime=''_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.cancelOrder)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.cancelOrder "Link to this definition")
Cancel the order and return the Trade it belongs to.

Parameters:
*   **order** ([`Order`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order "ib_async.order.Order")) – The order to be canceled.

*   **manualCancelOrderTime** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – For audit trail.

Return type:
[`Trade`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Trade "ib_async.order.Trade") | [`None`](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")

reqGlobalCancel()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.reqGlobalCancel)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.reqGlobalCancel "Link to this definition")
Cancel all active trades including those placed by other clients or TWS/IB gateway.

reqCurrentTime()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.reqCurrentTime)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.reqCurrentTime "Link to this definition")
Request TWS current time.

This method is blocking.

Return type:
[`datetime`](https://docs.python.org/3/library/datetime.html#datetime.datetime "(in Python v3.14)")

reqAccountUpdates(_account=''_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.reqAccountUpdates)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.reqAccountUpdates "Link to this definition")
This is called at startup - no need to call again.

Request account and portfolio values of the account and keep updated. Returns when both account values and portfolio are filled.

This method is blocking.

Parameters:
**account** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – If specified, filter for this account name.

reqAccountUpdatesMulti(_account=''_, _modelCode=''_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.reqAccountUpdatesMulti)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.reqAccountUpdatesMulti "Link to this definition")
It is recommended to use [`accountValues()`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.accountValues "ib_async.ib.IB.accountValues") instead.

Request account values of multiple accounts and keep updated.

This method is blocking.

Parameters:
*   **account** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – If specified, filter for this account name.

*   **modelCode** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – If specified, filter for this account model.

reqAccountSummary()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.reqAccountSummary)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.reqAccountSummary "Link to this definition")
It is recommended to use [`accountSummary()`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.accountSummary "ib_async.ib.IB.accountSummary") instead.

Request account values for all accounts and keep them updated. Returns when account summary is filled.

This method is blocking.

reqAutoOpenOrders(_autoBind=True_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.reqAutoOpenOrders)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.reqAutoOpenOrders "Link to this definition")
Bind manual TWS orders so that they can be managed from this client. The clientId must be 0 and the TWS API setting “Use negative numbers to bind automatic orders” must be checked.

This request is automatically called when clientId=0.

[https://interactivebrokers.github.io/tws-api/open_orders.html](https://interactivebrokers.github.io/tws-api/open_orders.html)[https://interactivebrokers.github.io/tws-api/modifying_orders.html](https://interactivebrokers.github.io/tws-api/modifying_orders.html)

Parameters:
**autoBind** ([`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")) – Set binding on or off.

reqOpenOrders()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.reqOpenOrders)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.reqOpenOrders "Link to this definition")
Request and return a list of open orders.

This method can give stale information where a new open order is not reported or an already filled or cancelled order is reported as open. It is recommended to use the more reliable and much faster [`openTrades()`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.openTrades "ib_async.ib.IB.openTrades") or [`openOrders()`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.openOrders "ib_async.ib.IB.openOrders") methods instead.

This method is blocking.

Return type:
[`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`Trade`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Trade "ib_async.order.Trade")]

reqAllOpenOrders()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.reqAllOpenOrders)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.reqAllOpenOrders "Link to this definition")
Request and return a list of all open orders over all clients. Note that the orders of other clients will not be kept in sync, use the master clientId mechanism instead to see other client’s orders that are kept in sync.

Return type:
[`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`Trade`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Trade "ib_async.order.Trade")]

reqCompletedOrders(_apiOnly_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.reqCompletedOrders)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.reqCompletedOrders "Link to this definition")
Request and return a list of completed trades.

Parameters:
**apiOnly** ([`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")) – Request only API orders (not manually placed TWS orders).

Return type:
[`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`Trade`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Trade "ib_async.order.Trade")]

reqExecutions(_execFilter=None_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.reqExecutions)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.reqExecutions "Link to this definition")
It is recommended to use [`fills()`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.fills "ib_async.ib.IB.fills") or [`executions()`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.executions "ib_async.ib.IB.executions") instead.

Request and return a list of fills.

This method is blocking.

Parameters:
**execFilter** ([`ExecutionFilter`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.ExecutionFilter "ib_async.objects.ExecutionFilter") | [`None`](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")) – If specified, return executions that match the filter.

Return type:
[`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`Fill`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.Fill "ib_async.objects.Fill")]

reqPositions()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.reqPositions)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.reqPositions "Link to this definition")
It is recommended to use [`positions()`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.positions "ib_async.ib.IB.positions") instead.

Request and return a list of positions for all accounts.

This method is blocking.

Return type:
[`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`Position`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.Position "ib_async.objects.Position")]

reqPnL(_account_, _modelCode=''_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.reqPnL)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.reqPnL "Link to this definition")
Start a subscription for profit and loss events.

Returns a [`PnL`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.PnL "ib_async.objects.PnL") object that is kept live updated. The result can also be queried from [`pnl()`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.pnl "ib_async.ib.IB.pnl").

[https://interactivebrokers.github.io/tws-api/pnl.html](https://interactivebrokers.github.io/tws-api/pnl.html)

Parameters:
*   **account** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – Subscribe to this account.

*   **modelCode** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – If specified, filter for this account model.

Return type:
[`PnL`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.PnL "ib_async.objects.PnL")

cancelPnL(_account_, _modelCode=''_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.cancelPnL)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.cancelPnL "Link to this definition")
Cancel PnL subscription.

Parameters:
*   **account** – Cancel for this account.

*   **modelCode** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – If specified, cancel for this account model.

reqPnLSingle(_account_, _modelCode_, _conId_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.reqPnLSingle)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.reqPnLSingle "Link to this definition")
Start a subscription for profit and loss events for single positions.

Returns a [`PnLSingle`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.PnLSingle "ib_async.objects.PnLSingle") object that is kept live updated. The result can also be queried from [`pnlSingle()`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.pnlSingle "ib_async.ib.IB.pnlSingle").

[https://interactivebrokers.github.io/tws-api/pnl.html](https://interactivebrokers.github.io/tws-api/pnl.html)

Parameters:
*   **account** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – Subscribe to this account.

*   **modelCode** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – Filter for this account model.

*   **conId** ([`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) – Filter for this contract ID.

Return type:
[`PnLSingle`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.PnLSingle "ib_async.objects.PnLSingle")

cancelPnLSingle(_account_, _modelCode_, _conId_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.cancelPnLSingle)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.cancelPnLSingle "Link to this definition")
Cancel PnLSingle subscription for the given account, modelCode and conId.

Parameters:
*   **account** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – Cancel for this account name.

*   **modelCode** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – Cancel for this account model.

*   **conId** ([`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) – Cancel for this contract ID.

reqContractDetails(_contract_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.reqContractDetails)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.reqContractDetails "Link to this definition")
Get a list of contract details that match the given contract. If the returned list is empty then the contract is not known; If the list has multiple values then the contract is ambiguous.

The fully qualified contract is available in the the ContractDetails.contract attribute.

This method is blocking.

[https://interactivebrokers.github.io/tws-api/contract_details.html](https://interactivebrokers.github.io/tws-api/contract_details.html)

Parameters:
**contract** ([`Contract`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Contract "ib_async.contract.Contract")) – The contract to get details for.

Return type:
[`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`ContractDetails`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ContractDetails "ib_async.contract.ContractDetails")]

reqMatchingSymbols(_pattern_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.reqMatchingSymbols)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.reqMatchingSymbols "Link to this definition")
Request contract descriptions of contracts that match a pattern.

This method is blocking.

[https://interactivebrokers.github.io/tws-api/matching_symbols.html](https://interactivebrokers.github.io/tws-api/matching_symbols.html)

Parameters:
**pattern** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – The first few letters of the ticker symbol, or for longer strings a character sequence matching a word in the security name.

Return type:
[`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`ContractDescription`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ContractDescription "ib_async.contract.ContractDescription")]

reqMarketRule(_marketRuleId_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.reqMarketRule)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.reqMarketRule "Link to this definition")
Request price increments rule.

[https://interactivebrokers.github.io/tws-api/minimum_increment.html](https://interactivebrokers.github.io/tws-api/minimum_increment.html)

Parameters:
**marketRuleId** ([`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) – ID of market rule. The market rule IDs for a contract can be obtained via [`reqContractDetails()`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.reqContractDetails "ib_async.ib.IB.reqContractDetails") from [`ContractDetails`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ContractDetails "ib_async.contract.ContractDetails").marketRuleIds, which contains a comma separated string of market rule IDs.

Return type:
[`PriceIncrement`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.PriceIncrement "ib_async.objects.PriceIncrement")

reqRealTimeBars(_contract_, _barSize_, _whatToShow_, _useRTH_, _realTimeBarsOptions=[]_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.reqRealTimeBars)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.reqRealTimeBars "Link to this definition")
Request realtime 5 second bars.

[https://interactivebrokers.github.io/tws-api/realtime_bars.html](https://interactivebrokers.github.io/tws-api/realtime_bars.html)

Parameters:
*   **contract** ([`Contract`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Contract "ib_async.contract.Contract")) – Contract of interest.

*   **barSize** ([`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) – Must be 5.

*   **whatToShow** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – Specifies the source for constructing bars. Can be ‘TRADES’, ‘MIDPOINT’, ‘BID’ or ‘ASK’.

*   **useRTH** ([`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")) – If True then only show data from within Regular Trading Hours, if False then show all data.

*   **realTimeBarsOptions** ([`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`TagValue`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.TagValue "ib_async.contract.TagValue")]) – Unknown.

Return type:
[`RealTimeBarList`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.RealTimeBarList "ib_async.objects.RealTimeBarList")

cancelRealTimeBars(_bars_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.cancelRealTimeBars)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.cancelRealTimeBars "Link to this definition")
Cancel the realtime bars subscription.

Parameters:
**bars** ([`RealTimeBarList`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.RealTimeBarList "ib_async.objects.RealTimeBarList")) – The bar list that was obtained from `reqRealTimeBars`.

reqHistoricalData(_contract_, _endDateTime_, _durationStr_, _barSizeSetting_, _whatToShow_, _useRTH_, _formatDate=1_, _keepUpToDate=False_, _chartOptions=[]_, _timeout=60_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.reqHistoricalData)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.reqHistoricalData "Link to this definition")
Request historical bar data.

This method is blocking.

[https://interactivebrokers.github.io/tws-api/historical_bars.html](https://interactivebrokers.github.io/tws-api/historical_bars.html)

Parameters:
*   **contract** ([`Contract`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Contract "ib_async.contract.Contract")) – Contract of interest.

*   **endDateTime** ([`datetime`](https://docs.python.org/3/library/datetime.html#datetime.datetime "(in Python v3.14)") | [`date`](https://docs.python.org/3/library/datetime.html#datetime.date "(in Python v3.14)") | [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [`None`](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")) – Can be set to ‘’ to indicate the current time, or it can be given as a datetime.date or datetime.datetime, or it can be given as a string in ‘yyyyMMdd HH:mm:ss’ format. If no timezone is given then the TWS login timezone is used.

*   **durationStr** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – Time span of all the bars. Examples: ‘60 S’, ‘30 D’, ‘13 W’, ‘6 M’, ‘10 Y’.

*   **barSizeSetting** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – Time period of one bar. Must be one of: ‘1 secs’, ‘5 secs’, ‘10 secs’ 15 secs’, ‘30 secs’, ‘1 min’, ‘2 mins’, ‘3 mins’, ‘5 mins’, ‘10 mins’, ‘15 mins’, ‘20 mins’, ‘30 mins’, ‘1 hour’, ‘2 hours’, ‘3 hours’, ‘4 hours’, ‘8 hours’, ‘1 day’, ‘1 week’, ‘1 month’.

*   **whatToShow** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – Specifies the source for constructing bars. Must be one of: ‘TRADES’, ‘MIDPOINT’, ‘BID’, ‘ASK’, ‘BID_ASK’, ‘ADJUSTED_LAST’, ‘HISTORICAL_VOLATILITY’, ‘OPTION_IMPLIED_VOLATILITY’, ‘REBATE_RATE’, ‘FEE_RATE’, ‘YIELD_BID’, ‘YIELD_ASK’, ‘YIELD_BID_ASK’, ‘YIELD_LAST’. For ‘SCHEDULE’ use [`reqHistoricalSchedule()`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.reqHistoricalSchedule "ib_async.ib.IB.reqHistoricalSchedule").

*   **useRTH** ([`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")) – If True then only show data from within Regular Trading Hours, if False then show all data.

*   **formatDate** ([`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) – For an intraday request setting to 2 will cause the returned date fields to be timezone-aware datetime.datetime with UTC timezone, instead of local timezone as used by TWS.

*   **keepUpToDate** ([`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")) – If True then a realtime subscription is started to keep the bars updated; `endDateTime` must be set empty (‘’) then.

*   **chartOptions** ([`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`TagValue`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.TagValue "ib_async.contract.TagValue")]) – Unknown.

*   **timeout** ([`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")) – Timeout in seconds after which to cancel the request and return an empty bar series. Set to `0` to wait indefinitely.

Return type:
[`BarDataList`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.BarDataList "ib_async.objects.BarDataList")

cancelHistoricalData(_bars_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.cancelHistoricalData)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.cancelHistoricalData "Link to this definition")
Cancel the update subscription for the historical bars.

Parameters:
**bars** ([`BarDataList`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.BarDataList "ib_async.objects.BarDataList")) – The bar list that was obtained from `reqHistoricalData` with a keepUpToDate subscription.

reqHistoricalSchedule(_contract_, _numDays_, _endDateTime=''_, _useRTH=True_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.reqHistoricalSchedule)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.reqHistoricalSchedule "Link to this definition")
Request historical schedule.

This method is blocking.

Parameters:
*   **contract** ([`Contract`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Contract "ib_async.contract.Contract")) – Contract of interest.

*   **numDays** ([`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) – Number of days.

*   **endDateTime** ([`datetime`](https://docs.python.org/3/library/datetime.html#datetime.datetime "(in Python v3.14)") | [`date`](https://docs.python.org/3/library/datetime.html#datetime.date "(in Python v3.14)") | [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [`None`](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")) – Can be set to ‘’ to indicate the current time, or it can be given as a datetime.date or datetime.datetime, or it can be given as a string in ‘yyyyMMdd HH:mm:ss’ format. If no timezone is given then the TWS login timezone is used.

*   **useRTH** ([`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")) – If True then show schedule for Regular Trading Hours, if False then for extended hours.

Return type:
[`HistoricalSchedule`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.HistoricalSchedule "ib_async.objects.HistoricalSchedule")

reqHistoricalTicks(_contract_, _startDateTime_, _endDateTime_, _numberOfTicks_, _whatToShow_, _useRth_, _ignoreSize=False_, _miscOptions=[]_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.reqHistoricalTicks)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.reqHistoricalTicks "Link to this definition")
Request historical ticks. The time resolution of the ticks is one second.

This method is blocking.

[https://interactivebrokers.github.io/tws-api/historical_time_and_sales.html](https://interactivebrokers.github.io/tws-api/historical_time_and_sales.html)

Parameters:
*   **contract** ([`Contract`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Contract "ib_async.contract.Contract")) – Contract to query.

*   **startDateTime** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [`date`](https://docs.python.org/3/library/datetime.html#datetime.date "(in Python v3.14)")) – Can be given as a datetime.date or datetime.datetime, or it can be given as a string in ‘yyyyMMdd HH:mm:ss’ format. If no timezone is given then the TWS login timezone is used.

*   **endDateTime** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [`date`](https://docs.python.org/3/library/datetime.html#datetime.date "(in Python v3.14)")) – One of `startDateTime` or `endDateTime` can be given, the other must be blank.

*   **numberOfTicks** ([`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) – Number of ticks to request (1000 max). The actual result can contain a bit more to accommodate all ticks in the latest second.

*   **whatToShow** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – One of ‘Bid_Ask’, ‘Midpoint’ or ‘Trades’.

*   **useRTH** – If True then only show data from within Regular Trading Hours, if False then show all data.

*   **ignoreSize** ([`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")) – Ignore bid/ask ticks that only update the size.

*   **miscOptions** ([`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`TagValue`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.TagValue "ib_async.contract.TagValue")]) – Unknown.

Return type:
[`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")

reqMarketDataType(_marketDataType_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.reqMarketDataType)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.reqMarketDataType "Link to this definition")
Set the market data type used for [`reqMktData()`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.reqMktData "ib_async.ib.IB.reqMktData").

Parameters:
**marketDataType** ([`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) –

One of:

*   1 = Live

*   2 = Frozen

*   3 = Delayed

*   4 = Delayed frozen

[https://interactivebrokers.github.io/tws-api/market_data_type.html](https://interactivebrokers.github.io/tws-api/market_data_type.html)

reqHeadTimeStamp(_contract_, _whatToShow_, _useRTH_, _formatDate=1_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.reqHeadTimeStamp)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.reqHeadTimeStamp "Link to this definition")
Get the datetime of earliest available historical data for the contract.

Parameters:
*   **contract** ([`Contract`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Contract "ib_async.contract.Contract")) – Contract of interest.

*   **useRTH** ([`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")) – If True then only show data from within Regular Trading Hours, if False then show all data.

*   **formatDate** ([`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) – If set to 2 then the result is returned as a timezone-aware datetime.datetime with UTC timezone.

Return type:
[`datetime`](https://docs.python.org/3/library/datetime.html#datetime.datetime "(in Python v3.14)")

reqMktData(_contract_, _genericTickList=''_, _snapshot=False_, _regulatorySnapshot=False_, _mktDataOptions=[]_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.reqMktData)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.reqMktData "Link to this definition")
Subscribe to tick data or request a snapshot. Returns the Ticker that holds the market data. The ticker will initially be empty and gradually (after a couple of seconds) be filled.

[https://interactivebrokers.github.io/tws-api/md_request.html](https://interactivebrokers.github.io/tws-api/md_request.html)

Parameters:
*   **contract** ([`Contract`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Contract "ib_async.contract.Contract")) – Contract of interest.

*   **genericTickList** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) –

Comma separated IDs of desired generic ticks that will cause corresponding Ticker fields to be filled:

| ID | Ticker fields |
| --- | --- |
| 100 | `putVolume`, `callVolume` (for options) |
| 101 | `putOpenInterest`, `callOpenInterest` (for options) |
| 104 | `histVolatility` (for options) |
| 105 | `avOptionVolume` (for options) |
| 106 | `impliedVolatility` (for options) |
| 162 | `indexFuturePremium` |
| 165 | `low13week`, `high13week`, `low26week`, `high26week`, `low52week`, `high52week`, `avVolume` |
| 221 | `markPrice` |
| 225 | `auctionVolume`, `auctionPrice`, `auctionImbalance` |
| 233 | `last`, `lastSize`, `rtVolume`, `rtTime`, `vwap` (Time & Sales) |
| 236 | `shortableShares` |
| 258 | `fundamentalRatios` (of type [`ib_async.objects.FundamentalRatios`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.FundamentalRatios "ib_async.objects.FundamentalRatios")) |
| 293 | `tradeCount` |
| 294 | `tradeRate` |
| 295 | `volumeRate` |
| 375 | `rtTradeVolume` |
| 411 | `rtHistVolatility` |
| 456 | `dividends` (of type [`ib_async.objects.Dividends`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.Dividends "ib_async.objects.Dividends")) |
| 588 | `futuresOpenInterest` |
*   **snapshot** ([`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")) – If True then request a one-time snapshot, otherwise subscribe to a stream of realtime tick data.

*   **regulatorySnapshot** ([`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")) – Request NBBO snapshot (may incur a fee).

*   **mktDataOptions** ([`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`TagValue`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.TagValue "ib_async.contract.TagValue")]) – Unknown

Return type:
[`Ticker`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker "ib_async.ticker.Ticker")

cancelMktData(_contract_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.cancelMktData)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.cancelMktData "Link to this definition")
Unsubscribe from realtime streaming tick data.

Parameters:
**contract** ([`Contract`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Contract "ib_async.contract.Contract")) – The contract of a previously subscribed ticker to unsubscribe.

Return type:
[`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")

Returns:
Returns True if cancel was successful. Returns False if ‘contract’ was not found.

reqTickByTickData(_contract_, _tickType_, _numberOfTicks=0_, _ignoreSize=False_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.reqTickByTickData)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.reqTickByTickData "Link to this definition")
Subscribe to tick-by-tick data and return the Ticker that holds the ticks in ticker.tickByTicks.

[https://interactivebrokers.github.io/tws-api/tick_data.html](https://interactivebrokers.github.io/tws-api/tick_data.html)

Parameters:
*   **contract** ([`Contract`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Contract "ib_async.contract.Contract")) – Contract of interest.

*   **tickType** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – One of ‘Last’, ‘AllLast’, ‘BidAsk’ or ‘MidPoint’.

*   **numberOfTicks** ([`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) – Number of ticks or 0 for unlimited.

*   **ignoreSize** ([`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")) – Ignore bid/ask ticks that only update the size.

Return type:
[`Ticker`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker "ib_async.ticker.Ticker")

cancelTickByTickData(_contract_, _tickType_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.cancelTickByTickData)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.cancelTickByTickData "Link to this definition")
Unsubscribe from tick-by-tick data

Parameters:
**contract** ([`Contract`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Contract "ib_async.contract.Contract")) – The contract of a previously subscribed ticker to unsubscribe.

Return type:
[`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")

Returns:
Returns True if cancel was successful. Returns False if ‘contract’ was not found.

reqSmartComponents(_bboExchange_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.reqSmartComponents)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.reqSmartComponents "Link to this definition")
Obtain mapping from single letter codes to exchange names.

Note: The exchanges must be open when using this request, otherwise an empty list is returned.

Return type:
[`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`SmartComponent`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.SmartComponent "ib_async.objects.SmartComponent")]

reqMktDepthExchanges()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.reqMktDepthExchanges)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.reqMktDepthExchanges "Link to this definition")
Get those exchanges that have have multiple market makers (and have ticks returned with marketMaker info).

Return type:
[`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`DepthMktDataDescription`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.DepthMktDataDescription "ib_async.objects.DepthMktDataDescription")]

reqMktDepth(_contract_, _numRows=5_, _isSmartDepth=False_, _mktDepthOptions=None_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.reqMktDepth)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.reqMktDepth "Link to this definition")
Subscribe to market depth data (a.k.a. DOM, L2 or order book).

[https://interactivebrokers.github.io/tws-api/market_depth.html](https://interactivebrokers.github.io/tws-api/market_depth.html)

Parameters:
*   **contract** ([`Contract`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Contract "ib_async.contract.Contract")) – Contract of interest.

*   **numRows** ([`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) – Number of depth level on each side of the order book (5 max).

*   **isSmartDepth** ([`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")) – Consolidate the order book across exchanges.

*   **mktDepthOptions** – Unknown.

Return type:
[`Ticker`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker "ib_async.ticker.Ticker")

Returns:
The Ticker that holds the market depth in `ticker.domBids` and `ticker.domAsks` and the list of MktDepthData in `ticker.domTicks`.

cancelMktDepth(_contract_, _isSmartDepth=False_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.cancelMktDepth)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.cancelMktDepth "Link to this definition")
Unsubscribe from market depth data.

Parameters:
**contract** ([`Contract`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Contract "ib_async.contract.Contract")) – The exact contract object that was used to subscribe with.

reqHistogramData(_contract_, _useRTH_, _period_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.reqHistogramData)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.reqHistogramData "Link to this definition")
Request histogram data.

This method is blocking.

[https://interactivebrokers.github.io/tws-api/histograms.html](https://interactivebrokers.github.io/tws-api/histograms.html)

Parameters:
*   **contract** ([`Contract`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Contract "ib_async.contract.Contract")) – Contract to query.

*   **useRTH** ([`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")) – If True then only show data from within Regular Trading Hours, if False then show all data.

*   **period** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – Period of which data is being requested, for example ‘3 days’.

Return type:
[`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`HistogramData`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.HistogramData "ib_async.objects.HistogramData")]

reqFundamentalData(_contract_, _reportType_, _fundamentalDataOptions=[]_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.reqFundamentalData)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.reqFundamentalData "Link to this definition")
Get fundamental data of a contract in XML format.

This method is blocking.

[https://interactivebrokers.github.io/tws-api/fundamentals.html](https://interactivebrokers.github.io/tws-api/fundamentals.html)

Parameters:
*   **contract** ([`Contract`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Contract "ib_async.contract.Contract")) – Contract to query.

*   **reportType** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) –

    *   ‘ReportsFinSummary’: Financial summary

    *   ’ReportsOwnership’: Company’s ownership

    *   ’ReportSnapshot’: Company’s financial overview

    *   ’ReportsFinStatements’: Financial Statements

    *   ’RESC’: Analyst Estimates

    *   ’CalendarReport’: Company’s calendar

*   **fundamentalDataOptions** ([`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`TagValue`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.TagValue "ib_async.contract.TagValue")]) – Unknown

Return type:
[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")

reqScannerData(_subscription_, _scannerSubscriptionOptions=[]_, _scannerSubscriptionFilterOptions=[]_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.reqScannerData)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.reqScannerData "Link to this definition")
Do a blocking market scan by starting a subscription and canceling it after the initial list of results are in.

This method is blocking.

[https://interactivebrokers.github.io/tws-api/market_scanners.html](https://interactivebrokers.github.io/tws-api/market_scanners.html)

Parameters:
*   **subscription** ([`ScannerSubscription`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.ScannerSubscription "ib_async.objects.ScannerSubscription")) – Basic filters.

*   **scannerSubscriptionOptions** ([`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`TagValue`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.TagValue "ib_async.contract.TagValue")]) – Unknown.

*   **scannerSubscriptionFilterOptions** ([`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`TagValue`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.TagValue "ib_async.contract.TagValue")]) – Advanced generic filters.

Return type:
[`ScanDataList`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.ScanDataList "ib_async.objects.ScanDataList")

reqScannerSubscription(_subscription_, _scannerSubscriptionOptions=[]_, _scannerSubscriptionFilterOptions=[]_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.reqScannerSubscription)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.reqScannerSubscription "Link to this definition")
Subscribe to market scan data.

[https://interactivebrokers.github.io/tws-api/market_scanners.html](https://interactivebrokers.github.io/tws-api/market_scanners.html)

Parameters:
*   **subscription** ([`ScannerSubscription`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.ScannerSubscription "ib_async.objects.ScannerSubscription")) – What to scan for.

*   **scannerSubscriptionOptions** ([`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`TagValue`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.TagValue "ib_async.contract.TagValue")]) – Unknown.

*   **scannerSubscriptionFilterOptions** ([`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`TagValue`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.TagValue "ib_async.contract.TagValue")]) – Unknown.

Return type:
[`ScanDataList`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.ScanDataList "ib_async.objects.ScanDataList")

cancelScannerSubscription(_dataList_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.cancelScannerSubscription)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.cancelScannerSubscription "Link to this definition")
Cancel market data subscription.

[https://interactivebrokers.github.io/tws-api/market_scanners.html](https://interactivebrokers.github.io/tws-api/market_scanners.html)

Parameters:
**dataList** ([`ScanDataList`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.ScanDataList "ib_async.objects.ScanDataList")) – The scan data list that was obtained from [`reqScannerSubscription()`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.reqScannerSubscription "ib_async.ib.IB.reqScannerSubscription").

reqScannerParameters()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.reqScannerParameters)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.reqScannerParameters "Link to this definition")
Requests an XML list of scanner parameters.

This method is blocking.

Return type:
[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")

calculateImpliedVolatility(_contract_, _optionPrice_, _underPrice_, _implVolOptions=[]_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.calculateImpliedVolatility)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.calculateImpliedVolatility "Link to this definition")
Calculate the volatility given the option price.

This method is blocking.

[https://interactivebrokers.github.io/tws-api/option_computations.html](https://interactivebrokers.github.io/tws-api/option_computations.html)

Parameters:
*   **contract** ([`Contract`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Contract "ib_async.contract.Contract")) – Option contract.

*   **optionPrice** ([`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")) – Option price to use in calculation.

*   **underPrice** ([`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")) – Price of the underlier to use in calculation

*   **implVolOptions** ([`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`TagValue`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.TagValue "ib_async.contract.TagValue")]) – Unknown

Return type:
[`OptionComputation`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.OptionComputation "ib_async.objects.OptionComputation")

calculateOptionPrice(_contract_, _volatility_, _underPrice_, _optPrcOptions=[]_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.calculateOptionPrice)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.calculateOptionPrice "Link to this definition")
Calculate the option price given the volatility.

This method is blocking.

[https://interactivebrokers.github.io/tws-api/option_computations.html](https://interactivebrokers.github.io/tws-api/option_computations.html)

Parameters:
*   **contract** ([`Contract`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Contract "ib_async.contract.Contract")) – Option contract.

*   **volatility** ([`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")) – Option volatility to use in calculation.

*   **underPrice** ([`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")) – Price of the underlier to use in calculation

*   **implVolOptions** – Unknown

Return type:
[`OptionComputation`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.OptionComputation "ib_async.objects.OptionComputation")

reqSecDefOptParams(_underlyingSymbol_, _futFopExchange_, _underlyingSecType_, _underlyingConId_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.reqSecDefOptParams)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.reqSecDefOptParams "Link to this definition")
Get the option chain.

This method is blocking.

[https://interactivebrokers.github.io/tws-api/options.html](https://interactivebrokers.github.io/tws-api/options.html)

Parameters:
*   **underlyingSymbol** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – Symbol of underlier contract.

*   **futFopExchange** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – Exchange (only for `FuturesOption`, otherwise leave blank).

*   **underlyingSecType** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – The type of the underlying security, like ‘STK’ or ‘FUT’.

*   **underlyingConId** ([`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) – conId of the underlying contract.

Return type:
[`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`OptionChain`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.OptionChain "ib_async.objects.OptionChain")]

exerciseOptions(_contract_, _exerciseAction_, _exerciseQuantity_, _account_, _override_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.exerciseOptions)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.exerciseOptions "Link to this definition")
Exercise an options contract.

[https://interactivebrokers.github.io/tws-api/options.html](https://interactivebrokers.github.io/tws-api/options.html)

Parameters:
*   **contract** ([`Contract`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Contract "ib_async.contract.Contract")) – The option contract to be exercised.

*   **exerciseAction** ([`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) –

    *   1 = exercise the option

    *   2 = let the option lapse

*   **exerciseQuantity** ([`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) – Number of contracts to be exercised.

*   **account** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – Destination account.

*   **override** ([`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) –

    *   0 = no override

    *   1 = override the system’s natural action

reqNewsProviders()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.reqNewsProviders)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.reqNewsProviders "Link to this definition")
Get a list of news providers.

This method is blocking.

Return type:
[`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`NewsProvider`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.NewsProvider "ib_async.objects.NewsProvider")]

reqNewsArticle(_providerCode_, _articleId_, _newsArticleOptions=[]_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.reqNewsArticle)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.reqNewsArticle "Link to this definition")
Get the body of a news article.

This method is blocking.

[https://interactivebrokers.github.io/tws-api/news.html](https://interactivebrokers.github.io/tws-api/news.html)

Parameters:
*   **providerCode** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – Code indicating news provider, like ‘BZ’ or ‘FLY’.

*   **articleId** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – ID of the specific article.

*   **newsArticleOptions** ([`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`TagValue`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.TagValue "ib_async.contract.TagValue")]) – Unknown.

Return type:
[`NewsArticle`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.NewsArticle "ib_async.objects.NewsArticle")

reqHistoricalNews(_conId_, _providerCodes_, _startDateTime_, _endDateTime_, _totalResults_, _historicalNewsOptions=[]_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.reqHistoricalNews)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.reqHistoricalNews "Link to this definition")
Get historical news headline.

[https://interactivebrokers.github.io/tws-api/news.html](https://interactivebrokers.github.io/tws-api/news.html)

This method is blocking.

Parameters:
*   **conId** ([`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) – Search news articles for contract with this conId.

*   **providerCodes** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – A ‘+’-separated list of provider codes, like ‘BZ+FLY’.

*   **startDateTime** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [`date`](https://docs.python.org/3/library/datetime.html#datetime.date "(in Python v3.14)")) – The (exclusive) start of the date range. Can be given as a datetime.date or datetime.datetime, or it can be given as a string in ‘yyyyMMdd HH:mm:ss’ format. If no timezone is given then the TWS login timezone is used.

*   **endDateTime** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [`date`](https://docs.python.org/3/library/datetime.html#datetime.date "(in Python v3.14)")) – The (inclusive) end of the date range. Can be given as a datetime.date or datetime.datetime, or it can be given as a string in ‘yyyyMMdd HH:mm:ss’ format. If no timezone is given then the TWS login timezone is used.

*   **totalResults** ([`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) – Maximum number of headlines to fetch (300 max).

*   **historicalNewsOptions** ([`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`TagValue`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.TagValue "ib_async.contract.TagValue")]) – Unknown.

Return type:
[`HistoricalNews`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.HistoricalNews "ib_async.objects.HistoricalNews")

reqNewsBulletins(_allMessages_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.reqNewsBulletins)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.reqNewsBulletins "Link to this definition")
Subscribe to IB news bulletins.

[https://interactivebrokers.github.io/tws-api/news.html](https://interactivebrokers.github.io/tws-api/news.html)

Parameters:
**allMessages** ([`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")) – If True then fetch all messages for the day.

cancelNewsBulletins()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.cancelNewsBulletins)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.cancelNewsBulletins "Link to this definition")
Cancel subscription to IB news bulletins.

requestFA(_faDataType_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.requestFA)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.requestFA "Link to this definition")
Requests to change the FA configuration.

This method is blocking.

Parameters:
**faDataType** ([`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) –

*   1 = Groups: Offer traders a way to create a group of accounts and apply a single allocation method to all accounts in the group.

*   2 = Profiles: Let you allocate shares on an account-by-account basis using a predefined calculation value.

*   3 = Account Aliases: Let you easily identify the accounts by meaningful names rather than account numbers.

replaceFA(_faDataType_, _xml_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.replaceFA)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.replaceFA "Link to this definition")
Replaces Financial Advisor’s settings.

Parameters:
*   **faDataType** ([`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) – See [`requestFA()`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.requestFA "ib_async.ib.IB.requestFA").

*   **xml** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – The XML-formatted configuration string.

reqWshMetaData()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.reqWshMetaData)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.reqWshMetaData "Link to this definition")
Request Wall Street Horizon metadata.

[https://interactivebrokers.github.io/tws-api/fundamentals.html](https://interactivebrokers.github.io/tws-api/fundamentals.html)

cancelWshMetaData()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.cancelWshMetaData)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.cancelWshMetaData "Link to this definition")
Cancel WSH metadata.

reqWshEventData(_data_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.reqWshEventData)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.reqWshEventData "Link to this definition")
Request Wall Street Horizon event data.

[`reqWshMetaData()`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.reqWshMetaData "ib_async.ib.IB.reqWshMetaData") must have been called first before using this method.

Parameters:
**data** ([`WshEventData`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.WshEventData "ib_async.objects.WshEventData")) – Filters for selecting the corporate event data.

[https://interactivebrokers.github.io/tws-api/wshe_filters.html](https://interactivebrokers.github.io/tws-api/wshe_filters.html)

cancelWshEventData()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.cancelWshEventData)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.cancelWshEventData "Link to this definition")
Cancel active WHS event data.

getWshMetaData()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.getWshMetaData)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.getWshMetaData "Link to this definition")
Blocking convenience method that returns the WSH metadata (that is the available filters and event types) as a JSON string.

Please note that a [Wall Street Horizon subscription](https://www.wallstreethorizon.com/interactive-brokers) is required.

# Get the list of available filters and event types:
meta = ib.getWshMetaData()
print(meta)

Return type:
[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")

getWshEventData(_data_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.getWshEventData)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.getWshEventData "Link to this definition")
Blocking convenience method that returns the WSH event data as a JSON string. [`getWshMetaData()`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.getWshMetaData "ib_async.ib.IB.getWshMetaData") must have been called first before using this method.

Please note that a [Wall Street Horizon subscription](https://www.wallstreethorizon.com/interactive-brokers) is required.

# For IBM (with conId=8314) query the:
# - Earnings Dates (wshe_ed)
# - Board of Directors meetings (wshe_bod)
data = WshEventData(
    filter = '''{
 "country": "All",
 "watchlist": ["8314"],
 "limit_region": 10,
 "limit": 10,
 "wshe_ed": "true",
 "wshe_bod": "true"
 }''')
events = ib.getWshEventData(data)
print(events)

Return type:
[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")

reqUserInfo()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.reqUserInfo)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.reqUserInfo "Link to this definition")
Get the White Branding ID of the user.

Return type:
[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")

_async_ connectAsync(_host='127.0.0.1'_, _port=7497_, _clientId=1_, _timeout=4_, _readonly=False_, _account=''_, _raiseSyncErrors=False_, _fetchFields=<StartupFetch.POSITIONS|ORDERS\_OPEN|ORDERS\_COMPLETE|ACCOUNT\_UPDATES|SUB\_ACCOUNT\_UPDATES|EXECUTIONS:63>_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.connectAsync)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.connectAsync "Link to this definition")_async_ qualifyContractsAsync(_*contracts_, _returnAll=False_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.qualifyContractsAsync)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.qualifyContractsAsync "Link to this definition")
Looks up all contract details, but only returns matching Contract objects.

If ‘returnAll’ is True, instead of returning ‘None’ on an ambiguous contract request, the return slot will have a list of the matching contracts. Previously the conflicts were only sent to the log, which isn’t useful if you are logging to a file and not watching immediately.

Return type:
[`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`Contract`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Contract "ib_async.contract.Contract") | [`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`Contract`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Contract "ib_async.contract.Contract") | [`None`](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")] | [`None`](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")]

Note: return value has elements in same position as input request. If a contract
cannot be qualified (bad values, ambiguous), the return value for the contract position in the result is None.

_async_ reqTickersAsync(_*contracts_, _regulatorySnapshot=False_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.reqTickersAsync)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.reqTickersAsync "Link to this definition")Return type:
[`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`Ticker`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker "ib_async.ticker.Ticker")]

whatIfOrderAsync(_contract_, _order_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.whatIfOrderAsync)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.whatIfOrderAsync "Link to this definition")Return type:
[`Awaitable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Awaitable "(in Python v3.14)")[[`OrderState`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderState "ib_async.order.OrderState")]

reqCurrentTimeAsync()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.reqCurrentTimeAsync)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.reqCurrentTimeAsync "Link to this definition")Return type:
[`Awaitable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Awaitable "(in Python v3.14)")[[`datetime`](https://docs.python.org/3/library/datetime.html#datetime.datetime "(in Python v3.14)")]

reqAccountUpdatesAsync(_account_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.reqAccountUpdatesAsync)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.reqAccountUpdatesAsync "Link to this definition")Return type:
[`Awaitable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Awaitable "(in Python v3.14)")[[`None`](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")]

reqAccountUpdatesMultiAsync(_account_, _modelCode=''_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.reqAccountUpdatesMultiAsync)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.reqAccountUpdatesMultiAsync "Link to this definition")Return type:
[`Awaitable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Awaitable "(in Python v3.14)")[[`None`](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")]

_async_ accountSummaryAsync(_account=''_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.accountSummaryAsync)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.accountSummaryAsync "Link to this definition")Return type:
[`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`AccountValue`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.AccountValue "ib_async.objects.AccountValue")]

reqAccountSummaryAsync()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.reqAccountSummaryAsync)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.reqAccountSummaryAsync "Link to this definition")Return type:
[`Awaitable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Awaitable "(in Python v3.14)")[[`None`](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")]

reqOpenOrdersAsync()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.reqOpenOrdersAsync)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.reqOpenOrdersAsync "Link to this definition")Return type:
[`Awaitable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Awaitable "(in Python v3.14)")[[`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`Trade`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Trade "ib_async.order.Trade")]]

reqAllOpenOrdersAsync()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.reqAllOpenOrdersAsync)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.reqAllOpenOrdersAsync "Link to this definition")Return type:
[`Awaitable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Awaitable "(in Python v3.14)")[[`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`Trade`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Trade "ib_async.order.Trade")]]

reqCompletedOrdersAsync(_apiOnly_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.reqCompletedOrdersAsync)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.reqCompletedOrdersAsync "Link to this definition")Return type:
[`Awaitable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Awaitable "(in Python v3.14)")[[`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`Trade`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Trade "ib_async.order.Trade")]]

reqExecutionsAsync(_execFilter=None_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.reqExecutionsAsync)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.reqExecutionsAsync "Link to this definition")Return type:
[`Awaitable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Awaitable "(in Python v3.14)")[[`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`Fill`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.Fill "ib_async.objects.Fill")]]

reqPositionsAsync()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.reqPositionsAsync)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.reqPositionsAsync "Link to this definition")Return type:
[`Awaitable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Awaitable "(in Python v3.14)")[[`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`Position`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.Position "ib_async.objects.Position")]]

reqContractDetailsAsync(_contract_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.reqContractDetailsAsync)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.reqContractDetailsAsync "Link to this definition")Return type:
[`Awaitable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Awaitable "(in Python v3.14)")[[`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`ContractDetails`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ContractDetails "ib_async.contract.ContractDetails")]]

_async_ reqMatchingSymbolsAsync(_pattern_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.reqMatchingSymbolsAsync)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.reqMatchingSymbolsAsync "Link to this definition")Return type:
[`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`ContractDescription`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ContractDescription "ib_async.contract.ContractDescription")] | [`None`](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")

_async_ reqMarketRuleAsync(_marketRuleId_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.reqMarketRuleAsync)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.reqMarketRuleAsync "Link to this definition")Return type:
[`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`PriceIncrement`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.PriceIncrement "ib_async.objects.PriceIncrement")] | [`None`](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")

_async_ reqHistoricalDataAsync(_contract_, _endDateTime_, _durationStr_, _barSizeSetting_, _whatToShow_, _useRTH_, _formatDate=1_, _keepUpToDate=False_, _chartOptions=[]_, _timeout=60_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.reqHistoricalDataAsync)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.reqHistoricalDataAsync "Link to this definition")Return type:
[`BarDataList`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.BarDataList "ib_async.objects.BarDataList")

reqHistoricalScheduleAsync(_contract_, _numDays_, _endDateTime=''_, _useRTH=True_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.reqHistoricalScheduleAsync)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.reqHistoricalScheduleAsync "Link to this definition")Return type:
[`Awaitable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Awaitable "(in Python v3.14)")[[`HistoricalSchedule`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.HistoricalSchedule "ib_async.objects.HistoricalSchedule")]

reqHistoricalTicksAsync(_contract_, _startDateTime_, _endDateTime_, _numberOfTicks_, _whatToShow_, _useRth_, _ignoreSize=False_, _miscOptions=[]_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.reqHistoricalTicksAsync)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.reqHistoricalTicksAsync "Link to this definition")Return type:
[`Awaitable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Awaitable "(in Python v3.14)")[[`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")]

_async_ reqHeadTimeStampAsync(_contract_, _whatToShow_, _useRTH_, _formatDate_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.reqHeadTimeStampAsync)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.reqHeadTimeStampAsync "Link to this definition")Return type:
[`datetime`](https://docs.python.org/3/library/datetime.html#datetime.datetime "(in Python v3.14)")

reqSmartComponentsAsync(_bboExchange_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.reqSmartComponentsAsync)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.reqSmartComponentsAsync "Link to this definition")reqMktDepthExchangesAsync()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.reqMktDepthExchangesAsync)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.reqMktDepthExchangesAsync "Link to this definition")Return type:
[`Awaitable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Awaitable "(in Python v3.14)")[[`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`DepthMktDataDescription`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.DepthMktDataDescription "ib_async.objects.DepthMktDataDescription")]]

reqHistogramDataAsync(_contract_, _useRTH_, _period_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.reqHistogramDataAsync)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.reqHistogramDataAsync "Link to this definition")Return type:
[`Awaitable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Awaitable "(in Python v3.14)")[[`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`HistogramData`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.HistogramData "ib_async.objects.HistogramData")]]

reqFundamentalDataAsync(_contract_, _reportType_, _fundamentalDataOptions=[]_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.reqFundamentalDataAsync)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.reqFundamentalDataAsync "Link to this definition")Return type:
[`Awaitable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Awaitable "(in Python v3.14)")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")]

_async_ reqScannerDataAsync(_subscription_, _scannerSubscriptionOptions=[]_, _scannerSubscriptionFilterOptions=[]_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.reqScannerDataAsync)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.reqScannerDataAsync "Link to this definition")Return type:
[`ScanDataList`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.ScanDataList "ib_async.objects.ScanDataList")

reqScannerParametersAsync()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.reqScannerParametersAsync)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.reqScannerParametersAsync "Link to this definition")Return type:
[`Awaitable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Awaitable "(in Python v3.14)")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")]

_async_ calculateImpliedVolatilityAsync(_contract_, _optionPrice_, _underPrice_, _implVolOptions=[]_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.calculateImpliedVolatilityAsync)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.calculateImpliedVolatilityAsync "Link to this definition")Return type:
[`OptionComputation`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.OptionComputation "ib_async.objects.OptionComputation") | [`None`](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")

_async_ calculateOptionPriceAsync(_contract_, _volatility_, _underPrice_, _optPrcOptions=[]_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.calculateOptionPriceAsync)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.calculateOptionPriceAsync "Link to this definition")Return type:
[`OptionComputation`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.OptionComputation "ib_async.objects.OptionComputation") | [`None`](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")

reqSecDefOptParamsAsync(_underlyingSymbol_, _futFopExchange_, _underlyingSecType_, _underlyingConId_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.reqSecDefOptParamsAsync)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.reqSecDefOptParamsAsync "Link to this definition")Return type:
[`Awaitable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Awaitable "(in Python v3.14)")[[`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`OptionChain`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.OptionChain "ib_async.objects.OptionChain")]]

reqNewsProvidersAsync()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.reqNewsProvidersAsync)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.reqNewsProvidersAsync "Link to this definition")Return type:
[`Awaitable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Awaitable "(in Python v3.14)")[[`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`NewsProvider`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.NewsProvider "ib_async.objects.NewsProvider")]]

reqNewsArticleAsync(_providerCode_, _articleId_, _newsArticleOptions=[]_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.reqNewsArticleAsync)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.reqNewsArticleAsync "Link to this definition")Return type:
[`Awaitable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Awaitable "(in Python v3.14)")[[`NewsArticle`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.NewsArticle "ib_async.objects.NewsArticle")]

_async_ reqHistoricalNewsAsync(_conId_, _providerCodes_, _startDateTime_, _endDateTime_, _totalResults_, _historicalNewsOptions=[]_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.reqHistoricalNewsAsync)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.reqHistoricalNewsAsync "Link to this definition")Return type:
[`HistoricalNews`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.HistoricalNews "ib_async.objects.HistoricalNews") | [`None`](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")

_async_ requestFAAsync(_faDataType_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.requestFAAsync)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.requestFAAsync "Link to this definition")_async_ getWshMetaDataAsync()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.getWshMetaDataAsync)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.getWshMetaDataAsync "Link to this definition")Return type:
[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")

_async_ getWshEventDataAsync(_data_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.getWshEventDataAsync)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.getWshEventDataAsync "Link to this definition")Return type:
[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")

reqUserInfoAsync()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ib.html#IB.reqUserInfoAsync)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB.reqUserInfoAsync "Link to this definition")
Client[](https://ib-api-reloaded.github.io/ib_async/api.html#module-ib_async.client "Link to this heading")
------------------------------------------------------------------------------------------------------------

Socket client for communicating with Interactive Brokers.

_class_ ib_async.client.Client(_wrapper_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client "Link to this definition")
Replacement for `ibapi.client.EClient` that uses asyncio.

The client is fully asynchronous and has its own event-driven networking code that replaces the networking code of the standard EClient. It also replaces the infinite loop of `EClient.run()` with the asyncio event loop. It can be used as a drop-in replacement for the standard EClient as provided by IBAPI.

Compared to the standard EClient this client has the following additional features:

*   `client.connect()` will block until the client is ready to serve requests; It is not necessary to wait for `nextValidId` to start requests as the client has already done that. The reqId is directly available with [`getReqId()`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.getReqId "ib_async.client.Client.getReqId").

*   `client.connectAsync()` is a coroutine for connecting asynchronously.

*   When blocking, `client.connect()` can be made to time out with the timeout parameter (default 2 seconds).

*   Optional `wrapper.priceSizeTick(reqId, tickType, price, size)` that combines price and size instead of the two wrapper methods priceTick and sizeTick.

*   Automatic request throttling.

*   Optional `wrapper.tcpDataArrived()` method; If the wrapper has this method it is invoked directly after a network packet has arrived. A possible use is to timestamp all data in the packet with the exact same time.

*   Optional `wrapper.tcpDataProcessed()` method; If the wrapper has this method it is invoked after the network packet’s data has been handled. A possible use is to write or evaluate the newly arrived data in one batch instead of item by item.

Parameters:
*   **MaxRequests** ([_int_](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) – Throttle the number of requests to `MaxRequests` per `RequestsInterval` seconds. Set to 0 to disable throttling.

*   **RequestsInterval** ([_float_](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")) – Time interval (in seconds) for request throttling.

*   **MinClientVersion** ([_int_](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) – Client protocol version.

*   **MaxClientVersion** ([_int_](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) – Client protocol version.

Events:
*   `apiStart` ()

*   `apiEnd` ()

*   `apiError` (errorMsg: str)

*   `throttleStart` ()

*   `throttleEnd` ()

events _=('apiStart','apiEnd','apiError','throttleStart','throttleEnd')_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.events "Link to this definition")MaxRequests _=45_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.MaxRequests "Link to this definition")RequestsInterval _=1_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.RequestsInterval "Link to this definition")MinClientVersion _=157_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.MinClientVersion "Link to this definition")MaxClientVersion _=178_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.MaxClientVersion "Link to this definition")DISCONNECTED _=0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.DISCONNECTED "Link to this definition")CONNECTING _=1_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.CONNECTING "Link to this definition")CONNECTED _=2_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.CONNECTED "Link to this definition")reset()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.reset)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.reset "Link to this definition")serverVersion()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.serverVersion)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.serverVersion "Link to this definition")Return type:
[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")

run()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.run)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.run "Link to this definition")isConnected()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.isConnected)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.isConnected "Link to this definition")isReady()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.isReady)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.isReady "Link to this definition")
Is the API connection up and running?

Return type:
[`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")

connectionStats()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.connectionStats)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.connectionStats "Link to this definition")
Get statistics about the connection.

Return type:
[`ConnectionStats`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.ConnectionStats "ib_async.objects.ConnectionStats")

getReqId()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.getReqId)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.getReqId "Link to this definition")
Get new request ID.

Return type:
[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")

updateReqId(_minReqId_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.updateReqId)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.updateReqId "Link to this definition")
Update the next reqId to be at least `minReqId`.

getAccounts()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.getAccounts)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.getAccounts "Link to this definition")
Get the list of account names that are under management.

Return type:
[`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")]

setConnectOptions(_connectOptions_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.setConnectOptions)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.setConnectOptions "Link to this definition")
Set additional connect options.

Parameters:
**connectOptions** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – Use “+PACEAPI” to use request-pacing built into TWS/gateway 974+ (obsolete).

connect(_host_, _port_, _clientId_, _timeout=2.0_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.connect)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.connect "Link to this definition")
Connect to a running TWS or IB gateway application.

Parameters:
*   **host** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – Host name or IP address.

*   **port** ([`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) – Port number.

*   **clientId** ([`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) – ID number to use for this client; must be unique per connection.

*   **timeout** ([`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)") | [`None`](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")) – If establishing the connection takes longer than `timeout` seconds then the `asyncio.TimeoutError` exception is raised. Set to 0 to disable timeout.

_async_ connectAsync(_host_, _port_, _clientId_, _timeout=2.0_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.connectAsync)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.connectAsync "Link to this definition")disconnect()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.disconnect)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.disconnect "Link to this definition")
Disconnect from IB connection.

send(_*fields_, _makeEmpty=True_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.send)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.send "Link to this definition")
Serialize and send the given fields using the IB socket protocol.

if ‘makeEmpty’ is True (default), then the IBKR values representing “no value” become the empty string.

sendMsg(_msg_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.sendMsg)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.sendMsg "Link to this definition")reqMktData(_reqId_, _contract_, _genericTickList_, _snapshot_, _regulatorySnapshot_, _mktDataOptions_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.reqMktData)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.reqMktData "Link to this definition")cancelMktData(_reqId_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.cancelMktData)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.cancelMktData "Link to this definition")placeOrder(_orderId_, _contract_, _order_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.placeOrder)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.placeOrder "Link to this definition")cancelOrder(_orderId_, _manualCancelOrderTime=''_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.cancelOrder)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.cancelOrder "Link to this definition")reqOpenOrders()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.reqOpenOrders)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.reqOpenOrders "Link to this definition")reqAccountUpdates(_subscribe_, _acctCode_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.reqAccountUpdates)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.reqAccountUpdates "Link to this definition")reqExecutions(_reqId_, _execFilter_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.reqExecutions)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.reqExecutions "Link to this definition")reqIds(_numIds_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.reqIds)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.reqIds "Link to this definition")reqContractDetails(_reqId_, _contract_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.reqContractDetails)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.reqContractDetails "Link to this definition")reqMktDepth(_reqId_, _contract_, _numRows_, _isSmartDepth_, _mktDepthOptions_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.reqMktDepth)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.reqMktDepth "Link to this definition")cancelMktDepth(_reqId_, _isSmartDepth_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.cancelMktDepth)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.cancelMktDepth "Link to this definition")reqNewsBulletins(_allMsgs_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.reqNewsBulletins)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.reqNewsBulletins "Link to this definition")cancelNewsBulletins()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.cancelNewsBulletins)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.cancelNewsBulletins "Link to this definition")setServerLogLevel(_logLevel_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.setServerLogLevel)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.setServerLogLevel "Link to this definition")reqAutoOpenOrders(_bAutoBind_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.reqAutoOpenOrders)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.reqAutoOpenOrders "Link to this definition")reqAllOpenOrders()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.reqAllOpenOrders)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.reqAllOpenOrders "Link to this definition")reqManagedAccts()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.reqManagedAccts)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.reqManagedAccts "Link to this definition")requestFA(_faData_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.requestFA)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.requestFA "Link to this definition")replaceFA(_reqId_, _faData_, _cxml_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.replaceFA)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.replaceFA "Link to this definition")reqHistoricalData(_reqId_, _contract_, _endDateTime_, _durationStr_, _barSizeSetting_, _whatToShow_, _useRTH_, _formatDate_, _keepUpToDate_, _chartOptions_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.reqHistoricalData)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.reqHistoricalData "Link to this definition")exerciseOptions(_reqId_, _contract_, _exerciseAction_, _exerciseQuantity_, _account_, _override_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.exerciseOptions)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.exerciseOptions "Link to this definition")reqScannerSubscription(_reqId_, _subscription_, _scannerSubscriptionOptions_, _scannerSubscriptionFilterOptions_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.reqScannerSubscription)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.reqScannerSubscription "Link to this definition")cancelScannerSubscription(_reqId_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.cancelScannerSubscription)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.cancelScannerSubscription "Link to this definition")reqScannerParameters()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.reqScannerParameters)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.reqScannerParameters "Link to this definition")cancelHistoricalData(_reqId_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.cancelHistoricalData)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.cancelHistoricalData "Link to this definition")reqCurrentTime()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.reqCurrentTime)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.reqCurrentTime "Link to this definition")reqRealTimeBars(_reqId_, _contract_, _barSize_, _whatToShow_, _useRTH_, _realTimeBarsOptions_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.reqRealTimeBars)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.reqRealTimeBars "Link to this definition")cancelRealTimeBars(_reqId_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.cancelRealTimeBars)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.cancelRealTimeBars "Link to this definition")reqFundamentalData(_reqId_, _contract_, _reportType_, _fundamentalDataOptions_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.reqFundamentalData)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.reqFundamentalData "Link to this definition")cancelFundamentalData(_reqId_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.cancelFundamentalData)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.cancelFundamentalData "Link to this definition")calculateImpliedVolatility(_reqId_, _contract_, _optionPrice_, _underPrice_, _implVolOptions_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.calculateImpliedVolatility)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.calculateImpliedVolatility "Link to this definition")calculateOptionPrice(_reqId_, _contract_, _volatility_, _underPrice_, _optPrcOptions_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.calculateOptionPrice)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.calculateOptionPrice "Link to this definition")cancelCalculateImpliedVolatility(_reqId_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.cancelCalculateImpliedVolatility)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.cancelCalculateImpliedVolatility "Link to this definition")cancelCalculateOptionPrice(_reqId_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.cancelCalculateOptionPrice)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.cancelCalculateOptionPrice "Link to this definition")reqGlobalCancel()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.reqGlobalCancel)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.reqGlobalCancel "Link to this definition")reqMarketDataType(_marketDataType_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.reqMarketDataType)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.reqMarketDataType "Link to this definition")reqPositions()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.reqPositions)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.reqPositions "Link to this definition")reqAccountSummary(_reqId_, _groupName_, _tags_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.reqAccountSummary)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.reqAccountSummary "Link to this definition")cancelAccountSummary(_reqId_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.cancelAccountSummary)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.cancelAccountSummary "Link to this definition")cancelPositions()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.cancelPositions)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.cancelPositions "Link to this definition")verifyRequest(_apiName_, _apiVersion_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.verifyRequest)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.verifyRequest "Link to this definition")verifyMessage(_apiData_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.verifyMessage)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.verifyMessage "Link to this definition")queryDisplayGroups(_reqId_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.queryDisplayGroups)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.queryDisplayGroups "Link to this definition")subscribeToGroupEvents(_reqId_, _groupId_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.subscribeToGroupEvents)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.subscribeToGroupEvents "Link to this definition")updateDisplayGroup(_reqId_, _contractInfo_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.updateDisplayGroup)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.updateDisplayGroup "Link to this definition")unsubscribeFromGroupEvents(_reqId_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.unsubscribeFromGroupEvents)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.unsubscribeFromGroupEvents "Link to this definition")startApi()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.startApi)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.startApi "Link to this definition")verifyAndAuthRequest(_apiName_, _apiVersion_, _opaqueIsvKey_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.verifyAndAuthRequest)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.verifyAndAuthRequest "Link to this definition")verifyAndAuthMessage(_apiData_, _xyzResponse_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.verifyAndAuthMessage)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.verifyAndAuthMessage "Link to this definition")reqPositionsMulti(_reqId_, _account_, _modelCode_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.reqPositionsMulti)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.reqPositionsMulti "Link to this definition")cancelPositionsMulti(_reqId_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.cancelPositionsMulti)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.cancelPositionsMulti "Link to this definition")reqAccountUpdatesMulti(_reqId_, _account_, _modelCode_, _ledgerAndNLV_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.reqAccountUpdatesMulti)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.reqAccountUpdatesMulti "Link to this definition")cancelAccountUpdatesMulti(_reqId_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.cancelAccountUpdatesMulti)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.cancelAccountUpdatesMulti "Link to this definition")reqSecDefOptParams(_reqId_, _underlyingSymbol_, _futFopExchange_, _underlyingSecType_, _underlyingConId_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.reqSecDefOptParams)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.reqSecDefOptParams "Link to this definition")reqSoftDollarTiers(_reqId_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.reqSoftDollarTiers)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.reqSoftDollarTiers "Link to this definition")reqFamilyCodes()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.reqFamilyCodes)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.reqFamilyCodes "Link to this definition")reqMatchingSymbols(_reqId_, _pattern_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.reqMatchingSymbols)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.reqMatchingSymbols "Link to this definition")reqMktDepthExchanges()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.reqMktDepthExchanges)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.reqMktDepthExchanges "Link to this definition")reqSmartComponents(_reqId_, _bboExchange_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.reqSmartComponents)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.reqSmartComponents "Link to this definition")reqNewsArticle(_reqId_, _providerCode_, _articleId_, _newsArticleOptions_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.reqNewsArticle)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.reqNewsArticle "Link to this definition")reqNewsProviders()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.reqNewsProviders)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.reqNewsProviders "Link to this definition")reqHistoricalNews(_reqId_, _conId_, _providerCodes_, _startDateTime_, _endDateTime_, _totalResults_, _historicalNewsOptions_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.reqHistoricalNews)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.reqHistoricalNews "Link to this definition")reqHeadTimeStamp(_reqId_, _contract_, _whatToShow_, _useRTH_, _formatDate_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.reqHeadTimeStamp)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.reqHeadTimeStamp "Link to this definition")reqHistogramData(_tickerId_, _contract_, _useRTH_, _timePeriod_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.reqHistogramData)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.reqHistogramData "Link to this definition")cancelHistogramData(_tickerId_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.cancelHistogramData)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.cancelHistogramData "Link to this definition")cancelHeadTimeStamp(_reqId_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.cancelHeadTimeStamp)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.cancelHeadTimeStamp "Link to this definition")reqMarketRule(_marketRuleId_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.reqMarketRule)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.reqMarketRule "Link to this definition")reqPnL(_reqId_, _account_, _modelCode_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.reqPnL)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.reqPnL "Link to this definition")cancelPnL(_reqId_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.cancelPnL)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.cancelPnL "Link to this definition")reqPnLSingle(_reqId_, _account_, _modelCode_, _conid_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.reqPnLSingle)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.reqPnLSingle "Link to this definition")cancelPnLSingle(_reqId_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.cancelPnLSingle)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.cancelPnLSingle "Link to this definition")reqHistoricalTicks(_reqId_, _contract_, _startDateTime_, _endDateTime_, _numberOfTicks_, _whatToShow_, _useRth_, _ignoreSize_, _miscOptions_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.reqHistoricalTicks)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.reqHistoricalTicks "Link to this definition")reqTickByTickData(_reqId_, _contract_, _tickType_, _numberOfTicks_, _ignoreSize_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.reqTickByTickData)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.reqTickByTickData "Link to this definition")cancelTickByTickData(_reqId_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.cancelTickByTickData)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.cancelTickByTickData "Link to this definition")reqCompletedOrders(_apiOnly_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.reqCompletedOrders)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.reqCompletedOrders "Link to this definition")reqWshMetaData(_reqId_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.reqWshMetaData)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.reqWshMetaData "Link to this definition")cancelWshMetaData(_reqId_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.cancelWshMetaData)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.cancelWshMetaData "Link to this definition")reqWshEventData(_reqId_, _data_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.reqWshEventData)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.reqWshEventData "Link to this definition")cancelWshEventData(_reqId_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.cancelWshEventData)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.cancelWshEventData "Link to this definition")reqUserInfo(_reqId_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/client.html#Client.reqUserInfo)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.client.Client.reqUserInfo "Link to this definition")
Order[](https://ib-api-reloaded.github.io/ib_async/api.html#module-ib_async.order "Link to this heading")
----------------------------------------------------------------------------------------------------------

Order types used by Interactive Brokers.

_class_ ib_async.order.Order(_orderId=0_, _clientId=0_, _permId=0_, _action=''_, _totalQuantity=0.0_, _orderType=''_, _lmtPrice=1.7976931348623157e+308_, _auxPrice=1.7976931348623157e+308_, _tif=''_, _activeStartTime=''_, _activeStopTime=''_, _ocaGroup=''_, _ocaType=0_, _orderRef=''_, _transmit=True_, _parentId=0_, _blockOrder=False_, _sweepToFill=False_, _displaySize=0_, _triggerMethod=0_, _outsideRth=False_, _hidden=False_, _goodAfterTime=''_, _goodTillDate=''_, _rule80A=''_, _allOrNone=False_, _minQty=2147483647_, _percentOffset=1.7976931348623157e+308_, _overridePercentageConstraints=False_, _trailStopPrice=1.7976931348623157e+308_, _trailingPercent=1.7976931348623157e+308_, _faGroup=''_, _faProfile=''_, _faMethod=''_, _faPercentage=''_, _designatedLocation=''_, _openClose='O'_, _origin=0_, _shortSaleSlot=0_, _exemptCode=-1_, _discretionaryAmt=0.0_, _eTradeOnly=False_, _firmQuoteOnly=False_, _nbboPriceCap=1.7976931348623157e+308_, _optOutSmartRouting=False_, _auctionStrategy=0_, _startingPrice=1.7976931348623157e+308_, _stockRefPrice=1.7976931348623157e+308_, _delta=1.7976931348623157e+308_, _stockRangeLower=1.7976931348623157e+308_, _stockRangeUpper=1.7976931348623157e+308_, _randomizePrice=False_, _randomizeSize=False_, _volatility=1.7976931348623157e+308_, _volatilityType=2147483647_, _deltaNeutralOrderType=''_, _deltaNeutralAuxPrice=1.7976931348623157e+308_, _deltaNeutralConId=0_, _deltaNeutralSettlingFirm=''_, _deltaNeutralClearingAccount=''_, _deltaNeutralClearingIntent=''_, _deltaNeutralOpenClose=''_, _deltaNeutralShortSale=False_, _deltaNeutralShortSaleSlot=0_, _deltaNeutralDesignatedLocation=''_, _continuousUpdate=False_, _referencePriceType=2147483647_, _basisPoints=1.7976931348623157e+308_, _basisPointsType=2147483647_, _scaleInitLevelSize=2147483647_, _scaleSubsLevelSize=2147483647_, _scalePriceIncrement=1.7976931348623157e+308_, _scalePriceAdjustValue=1.7976931348623157e+308_, _scalePriceAdjustInterval=2147483647_, _scaleProfitOffset=1.7976931348623157e+308_, _scaleAutoReset=False_, _scaleInitPosition=2147483647_, _scaleInitFillQty=2147483647_, _scaleRandomPercent=False_, _scaleTable=''_, _hedgeType=''_, _hedgeParam=''_, _account=''_, _settlingFirm=''_, _clearingAccount=''_, _clearingIntent=''_, _algoStrategy=''_, _algoParams=<factory>_, _smartComboRoutingParams=<factory>_, _algoId=''_, _whatIf=False_, _notHeld=False_, _solicited=False_, _modelCode=''_, _orderComboLegs=<factory>_, _orderMiscOptions=<factory>_, _referenceContractId=0_, _peggedChangeAmount=0.0_, _isPeggedChangeAmountDecrease=False_, _referenceChangeAmount=0.0_, _referenceExchangeId=''_, _adjustedOrderType=''_, _triggerPrice=1.7976931348623157e+308_, _adjustedStopPrice=1.7976931348623157e+308_, _adjustedStopLimitPrice=1.7976931348623157e+308_, _adjustedTrailingAmount=1.7976931348623157e+308_, _adjustableTrailingUnit=0_, _lmtPriceOffset=1.7976931348623157e+308_, _conditions=<factory>_, _conditionsCancelOrder=False_, _conditionsIgnoreRth=False_, _extOperator=''_, _softDollarTier=<factory>_, _cashQty=1.7976931348623157e+308_, _mifid2DecisionMaker=''_, _mifid2DecisionAlgo=''_, _mifid2ExecutionTrader=''_, _mifid2ExecutionAlgo=''_, _dontUseAutoPriceForHedge=False_, _isOmsContainer=False_, _discretionaryUpToLimitPrice=False_, _autoCancelDate=''_, _filledQuantity=1.7976931348623157e+308_, _refFuturesConId=0_, _autoCancelParent=False_, _shareholder=''_, _imbalanceOnly=False_, _routeMarketableToBbo=False_, _parentPermId=0_, _usePriceMgmtAlgo=False_, _duration=2147483647_, _postToAts=2147483647_, _advancedErrorOverride=''_, _manualOrderTime=''_, _minTradeQty=2147483647_, _minCompeteSize=2147483647_, _competeAgainstBestOffset=1.7976931348623157e+308_, _midOffsetAtWhole=1.7976931348623157e+308_, _midOffsetAtHalf=1.7976931348623157e+308_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/order.html#Order)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order "Link to this definition")
Order for trading contracts.

[https://interactivebrokers.github.io/tws-api/available_orders.html](https://interactivebrokers.github.io/tws-api/available_orders.html)

orderId _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.orderId "Link to this definition")clientId _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.clientId "Link to this definition")permId _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.permId "Link to this definition")action _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.action "Link to this definition")totalQuantity _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=0.0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.totalQuantity "Link to this definition")orderType _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.orderType "Link to this definition")lmtPrice _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")|[`Decimal`](https://docs.python.org/3/library/decimal.html#decimal.Decimal "(in Python v3.14)")|[`None`](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")_ _=1.7976931348623157e+308_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.lmtPrice "Link to this definition")auxPrice _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")|[`Decimal`](https://docs.python.org/3/library/decimal.html#decimal.Decimal "(in Python v3.14)")|[`None`](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")_ _=1.7976931348623157e+308_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.auxPrice "Link to this definition")tif _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.tif "Link to this definition")activeStartTime _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.activeStartTime "Link to this definition")activeStopTime _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.activeStopTime "Link to this definition")ocaGroup _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.ocaGroup "Link to this definition")ocaType _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.ocaType "Link to this definition")orderRef _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.orderRef "Link to this definition")transmit _:[`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")_ _=True_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.transmit "Link to this definition")parentId _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.parentId "Link to this definition")blockOrder _:[`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")_ _=False_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.blockOrder "Link to this definition")sweepToFill _:[`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")_ _=False_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.sweepToFill "Link to this definition")displaySize _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.displaySize "Link to this definition")triggerMethod _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.triggerMethod "Link to this definition")outsideRth _:[`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")_ _=False_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.outsideRth "Link to this definition")hidden _:[`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")_ _=False_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.hidden "Link to this definition")goodAfterTime _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.goodAfterTime "Link to this definition")goodTillDate _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.goodTillDate "Link to this definition")rule80A _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.rule80A "Link to this definition")allOrNone _:[`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")_ _=False_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.allOrNone "Link to this definition")minQty _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=2147483647_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.minQty "Link to this definition")percentOffset _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")|[`Decimal`](https://docs.python.org/3/library/decimal.html#decimal.Decimal "(in Python v3.14)")_ _=1.7976931348623157e+308_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.percentOffset "Link to this definition")overridePercentageConstraints _:[`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")_ _=False_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.overridePercentageConstraints "Link to this definition")trailStopPrice _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")|[`Decimal`](https://docs.python.org/3/library/decimal.html#decimal.Decimal "(in Python v3.14)")_ _=1.7976931348623157e+308_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.trailStopPrice "Link to this definition")trailingPercent _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")|[`Decimal`](https://docs.python.org/3/library/decimal.html#decimal.Decimal "(in Python v3.14)")_ _=1.7976931348623157e+308_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.trailingPercent "Link to this definition")faGroup _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.faGroup "Link to this definition")faProfile _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.faProfile "Link to this definition")faMethod _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.faMethod "Link to this definition")faPercentage _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.faPercentage "Link to this definition")designatedLocation _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.designatedLocation "Link to this definition")openClose _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _='O'_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.openClose "Link to this definition")origin _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.origin "Link to this definition")shortSaleSlot _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.shortSaleSlot "Link to this definition")exemptCode _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=-1_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.exemptCode "Link to this definition")discretionaryAmt _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=0.0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.discretionaryAmt "Link to this definition")eTradeOnly _:[`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")_ _=False_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.eTradeOnly "Link to this definition")firmQuoteOnly _:[`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")_ _=False_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.firmQuoteOnly "Link to this definition")nbboPriceCap _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")|[`Decimal`](https://docs.python.org/3/library/decimal.html#decimal.Decimal "(in Python v3.14)")_ _=1.7976931348623157e+308_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.nbboPriceCap "Link to this definition")optOutSmartRouting _:[`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")_ _=False_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.optOutSmartRouting "Link to this definition")auctionStrategy _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.auctionStrategy "Link to this definition")startingPrice _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")|[`Decimal`](https://docs.python.org/3/library/decimal.html#decimal.Decimal "(in Python v3.14)")_ _=1.7976931348623157e+308_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.startingPrice "Link to this definition")stockRefPrice _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")|[`Decimal`](https://docs.python.org/3/library/decimal.html#decimal.Decimal "(in Python v3.14)")_ _=1.7976931348623157e+308_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.stockRefPrice "Link to this definition")delta _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")|[`Decimal`](https://docs.python.org/3/library/decimal.html#decimal.Decimal "(in Python v3.14)")_ _=1.7976931348623157e+308_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.delta "Link to this definition")stockRangeLower _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")|[`Decimal`](https://docs.python.org/3/library/decimal.html#decimal.Decimal "(in Python v3.14)")_ _=1.7976931348623157e+308_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.stockRangeLower "Link to this definition")stockRangeUpper _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")|[`Decimal`](https://docs.python.org/3/library/decimal.html#decimal.Decimal "(in Python v3.14)")_ _=1.7976931348623157e+308_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.stockRangeUpper "Link to this definition")randomizePrice _:[`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")_ _=False_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.randomizePrice "Link to this definition")randomizeSize _:[`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")_ _=False_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.randomizeSize "Link to this definition")volatility _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")|[`Decimal`](https://docs.python.org/3/library/decimal.html#decimal.Decimal "(in Python v3.14)")_ _=1.7976931348623157e+308_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.volatility "Link to this definition")volatilityType _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=2147483647_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.volatilityType "Link to this definition")deltaNeutralOrderType _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.deltaNeutralOrderType "Link to this definition")deltaNeutralAuxPrice _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")|[`Decimal`](https://docs.python.org/3/library/decimal.html#decimal.Decimal "(in Python v3.14)")_ _=1.7976931348623157e+308_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.deltaNeutralAuxPrice "Link to this definition")deltaNeutralConId _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.deltaNeutralConId "Link to this definition")deltaNeutralSettlingFirm _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.deltaNeutralSettlingFirm "Link to this definition")deltaNeutralClearingAccount _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.deltaNeutralClearingAccount "Link to this definition")deltaNeutralClearingIntent _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.deltaNeutralClearingIntent "Link to this definition")deltaNeutralOpenClose _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.deltaNeutralOpenClose "Link to this definition")deltaNeutralShortSale _:[`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")_ _=False_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.deltaNeutralShortSale "Link to this definition")deltaNeutralShortSaleSlot _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.deltaNeutralShortSaleSlot "Link to this definition")deltaNeutralDesignatedLocation _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.deltaNeutralDesignatedLocation "Link to this definition")continuousUpdate _:[`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")_ _=False_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.continuousUpdate "Link to this definition")referencePriceType _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=2147483647_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.referencePriceType "Link to this definition")basisPoints _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")|[`Decimal`](https://docs.python.org/3/library/decimal.html#decimal.Decimal "(in Python v3.14)")_ _=1.7976931348623157e+308_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.basisPoints "Link to this definition")basisPointsType _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=2147483647_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.basisPointsType "Link to this definition")scaleInitLevelSize _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=2147483647_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.scaleInitLevelSize "Link to this definition")scaleSubsLevelSize _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=2147483647_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.scaleSubsLevelSize "Link to this definition")scalePriceIncrement _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")|[`Decimal`](https://docs.python.org/3/library/decimal.html#decimal.Decimal "(in Python v3.14)")_ _=1.7976931348623157e+308_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.scalePriceIncrement "Link to this definition")scalePriceAdjustValue _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")|[`Decimal`](https://docs.python.org/3/library/decimal.html#decimal.Decimal "(in Python v3.14)")_ _=1.7976931348623157e+308_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.scalePriceAdjustValue "Link to this definition")scalePriceAdjustInterval _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=2147483647_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.scalePriceAdjustInterval "Link to this definition")scaleProfitOffset _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")|[`Decimal`](https://docs.python.org/3/library/decimal.html#decimal.Decimal "(in Python v3.14)")_ _=1.7976931348623157e+308_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.scaleProfitOffset "Link to this definition")scaleAutoReset _:[`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")_ _=False_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.scaleAutoReset "Link to this definition")scaleInitPosition _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=2147483647_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.scaleInitPosition "Link to this definition")scaleInitFillQty _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=2147483647_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.scaleInitFillQty "Link to this definition")scaleRandomPercent _:[`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")_ _=False_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.scaleRandomPercent "Link to this definition")scaleTable _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.scaleTable "Link to this definition")hedgeType _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.hedgeType "Link to this definition")hedgeParam _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.hedgeParam "Link to this definition")account _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.account "Link to this definition")settlingFirm _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.settlingFirm "Link to this definition")clearingAccount _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.clearingAccount "Link to this definition")clearingIntent _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.clearingIntent "Link to this definition")algoStrategy _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.algoStrategy "Link to this definition")algoParams _:[`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`TagValue`](https://ib-api-reloaded.github.io/ib\_async/api.html#ib\_async.contract.TagValue "ib\_async.contract.TagValue")]_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.algoParams "Link to this definition")smartComboRoutingParams _:[`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`TagValue`](https://ib-api-reloaded.github.io/ib\_async/api.html#ib\_async.contract.TagValue "ib\_async.contract.TagValue")]_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.smartComboRoutingParams "Link to this definition")algoId _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.algoId "Link to this definition")whatIf _:[`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")_ _=False_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.whatIf "Link to this definition")notHeld _:[`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")_ _=False_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.notHeld "Link to this definition")solicited _:[`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")_ _=False_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.solicited "Link to this definition")modelCode _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.modelCode "Link to this definition")orderComboLegs _:[`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`OrderComboLeg`](https://ib-api-reloaded.github.io/ib\_async/api.html#ib\_async.order.OrderComboLeg "ib\_async.order.OrderComboLeg")]_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.orderComboLegs "Link to this definition")orderMiscOptions _:[`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`TagValue`](https://ib-api-reloaded.github.io/ib\_async/api.html#ib\_async.contract.TagValue "ib\_async.contract.TagValue")]_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.orderMiscOptions "Link to this definition")referenceContractId _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.referenceContractId "Link to this definition")peggedChangeAmount _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=0.0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.peggedChangeAmount "Link to this definition")isPeggedChangeAmountDecrease _:[`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")_ _=False_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.isPeggedChangeAmountDecrease "Link to this definition")referenceChangeAmount _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=0.0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.referenceChangeAmount "Link to this definition")referenceExchangeId _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.referenceExchangeId "Link to this definition")adjustedOrderType _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.adjustedOrderType "Link to this definition")triggerPrice _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")|[`Decimal`](https://docs.python.org/3/library/decimal.html#decimal.Decimal "(in Python v3.14)")|[`None`](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")_ _=1.7976931348623157e+308_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.triggerPrice "Link to this definition")adjustedStopPrice _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")|[`Decimal`](https://docs.python.org/3/library/decimal.html#decimal.Decimal "(in Python v3.14)")_ _=1.7976931348623157e+308_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.adjustedStopPrice "Link to this definition")adjustedStopLimitPrice _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")|[`Decimal`](https://docs.python.org/3/library/decimal.html#decimal.Decimal "(in Python v3.14)")_ _=1.7976931348623157e+308_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.adjustedStopLimitPrice "Link to this definition")adjustedTrailingAmount _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")|[`Decimal`](https://docs.python.org/3/library/decimal.html#decimal.Decimal "(in Python v3.14)")_ _=1.7976931348623157e+308_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.adjustedTrailingAmount "Link to this definition")adjustableTrailingUnit _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.adjustableTrailingUnit "Link to this definition")lmtPriceOffset _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")|[`Decimal`](https://docs.python.org/3/library/decimal.html#decimal.Decimal "(in Python v3.14)")_ _=1.7976931348623157e+308_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.lmtPriceOffset "Link to this definition")conditions _:[`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`OrderCondition`](https://ib-api-reloaded.github.io/ib\_async/api.html#ib\_async.order.OrderCondition "ib\_async.order.OrderCondition")]_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.conditions "Link to this definition")conditionsCancelOrder _:[`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")_ _=False_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.conditionsCancelOrder "Link to this definition")conditionsIgnoreRth _:[`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")_ _=False_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.conditionsIgnoreRth "Link to this definition")extOperator _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.extOperator "Link to this definition")softDollarTier _:[`SoftDollarTier`](https://ib-api-reloaded.github.io/ib\_async/api.html#ib\_async.objects.SoftDollarTier "ib\_async.objects.SoftDollarTier")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.softDollarTier "Link to this definition")cashQty _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")|[`Decimal`](https://docs.python.org/3/library/decimal.html#decimal.Decimal "(in Python v3.14)")_ _=1.7976931348623157e+308_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.cashQty "Link to this definition")mifid2DecisionMaker _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.mifid2DecisionMaker "Link to this definition")mifid2DecisionAlgo _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.mifid2DecisionAlgo "Link to this definition")mifid2ExecutionTrader _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.mifid2ExecutionTrader "Link to this definition")mifid2ExecutionAlgo _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.mifid2ExecutionAlgo "Link to this definition")dontUseAutoPriceForHedge _:[`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")_ _=False_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.dontUseAutoPriceForHedge "Link to this definition")isOmsContainer _:[`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")_ _=False_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.isOmsContainer "Link to this definition")discretionaryUpToLimitPrice _:[`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")_ _=False_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.discretionaryUpToLimitPrice "Link to this definition")autoCancelDate _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.autoCancelDate "Link to this definition")filledQuantity _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")|[`Decimal`](https://docs.python.org/3/library/decimal.html#decimal.Decimal "(in Python v3.14)")_ _=1.7976931348623157e+308_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.filledQuantity "Link to this definition")refFuturesConId _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.refFuturesConId "Link to this definition")autoCancelParent _:[`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")_ _=False_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.autoCancelParent "Link to this definition")shareholder _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.shareholder "Link to this definition")imbalanceOnly _:[`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")_ _=False_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.imbalanceOnly "Link to this definition")routeMarketableToBbo _:[`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")_ _=False_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.routeMarketableToBbo "Link to this definition")parentPermId _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.parentPermId "Link to this definition")usePriceMgmtAlgo _:[`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")_ _=False_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.usePriceMgmtAlgo "Link to this definition")duration _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=2147483647_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.duration "Link to this definition")postToAts _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=2147483647_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.postToAts "Link to this definition")advancedErrorOverride _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.advancedErrorOverride "Link to this definition")manualOrderTime _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.manualOrderTime "Link to this definition")minTradeQty _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=2147483647_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.minTradeQty "Link to this definition")minCompeteSize _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=2147483647_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.minCompeteSize "Link to this definition")competeAgainstBestOffset _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")|[`Decimal`](https://docs.python.org/3/library/decimal.html#decimal.Decimal "(in Python v3.14)")_ _=1.7976931348623157e+308_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.competeAgainstBestOffset "Link to this definition")midOffsetAtWhole _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")|[`Decimal`](https://docs.python.org/3/library/decimal.html#decimal.Decimal "(in Python v3.14)")_ _=1.7976931348623157e+308_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.midOffsetAtWhole "Link to this definition")midOffsetAtHalf _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")|[`Decimal`](https://docs.python.org/3/library/decimal.html#decimal.Decimal "(in Python v3.14)")_ _=1.7976931348623157e+308_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.midOffsetAtHalf "Link to this definition")dict()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.dict "Link to this definition")
Return dataclass values as `dict`. This is a non-recursive variant of `dataclasses.asdict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.dict "ib_async.order.Order.dict")

nonDefaults()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.nonDefaults "Link to this definition")
For a `dataclass` instance get the fields that are different from the default values and return as `dict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.dict "ib_async.order.Order.dict")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)"), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")]

tuple()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.tuple "Link to this definition")
Return dataclass values as `tuple`. This is a non-recursive variant of `dataclasses.astuple`.

Return type:
[`tuple`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.tuple "ib_async.order.Order.tuple")[[`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)"), [`...`](https://docs.python.org/3/library/constants.html#Ellipsis "(in Python v3.14)")]

update(_*srcObjs_, _**kwargs_)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Order.update "Link to this definition")
Update fields of the given `dataclass` object from zero or more `dataclass` source objects and/or from keyword arguments.

Return type:
[`object`](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)")

_class_ ib_async.order.LimitOrder(_action_, _totalQuantity_, _lmtPrice_, _**kwargs_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/order.html#LimitOrder)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.LimitOrder "Link to this definition")dict()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.LimitOrder.dict "Link to this definition")
Return dataclass values as `dict`. This is a non-recursive variant of `dataclasses.asdict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.LimitOrder.dict "ib_async.order.LimitOrder.dict")

nonDefaults()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.LimitOrder.nonDefaults "Link to this definition")
For a `dataclass` instance get the fields that are different from the default values and return as `dict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.LimitOrder.dict "ib_async.order.LimitOrder.dict")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)"), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")]

tuple()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.LimitOrder.tuple "Link to this definition")
Return dataclass values as `tuple`. This is a non-recursive variant of `dataclasses.astuple`.

Return type:
[`tuple`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.LimitOrder.tuple "ib_async.order.LimitOrder.tuple")[[`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)"), [`...`](https://docs.python.org/3/library/constants.html#Ellipsis "(in Python v3.14)")]

update(_*srcObjs_, _**kwargs_)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.LimitOrder.update "Link to this definition")
Update fields of the given `dataclass` object from zero or more `dataclass` source objects and/or from keyword arguments.

Return type:
[`object`](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)")

_class_ ib_async.order.MarketOrder(_action_, _totalQuantity_, _**kwargs_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/order.html#MarketOrder)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.MarketOrder "Link to this definition")dict()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.MarketOrder.dict "Link to this definition")
Return dataclass values as `dict`. This is a non-recursive variant of `dataclasses.asdict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.MarketOrder.dict "ib_async.order.MarketOrder.dict")

nonDefaults()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.MarketOrder.nonDefaults "Link to this definition")
For a `dataclass` instance get the fields that are different from the default values and return as `dict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.MarketOrder.dict "ib_async.order.MarketOrder.dict")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)"), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")]

tuple()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.MarketOrder.tuple "Link to this definition")
Return dataclass values as `tuple`. This is a non-recursive variant of `dataclasses.astuple`.

Return type:
[`tuple`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.MarketOrder.tuple "ib_async.order.MarketOrder.tuple")[[`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)"), [`...`](https://docs.python.org/3/library/constants.html#Ellipsis "(in Python v3.14)")]

update(_*srcObjs_, _**kwargs_)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.MarketOrder.update "Link to this definition")
Update fields of the given `dataclass` object from zero or more `dataclass` source objects and/or from keyword arguments.

Return type:
[`object`](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)")

_class_ ib_async.order.StopOrder(_action_, _totalQuantity_, _stopPrice_, _**kwargs_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/order.html#StopOrder)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.StopOrder "Link to this definition")dict()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.StopOrder.dict "Link to this definition")
Return dataclass values as `dict`. This is a non-recursive variant of `dataclasses.asdict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.StopOrder.dict "ib_async.order.StopOrder.dict")

nonDefaults()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.StopOrder.nonDefaults "Link to this definition")
For a `dataclass` instance get the fields that are different from the default values and return as `dict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.StopOrder.dict "ib_async.order.StopOrder.dict")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)"), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")]

tuple()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.StopOrder.tuple "Link to this definition")
Return dataclass values as `tuple`. This is a non-recursive variant of `dataclasses.astuple`.

Return type:
[`tuple`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.StopOrder.tuple "ib_async.order.StopOrder.tuple")[[`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)"), [`...`](https://docs.python.org/3/library/constants.html#Ellipsis "(in Python v3.14)")]

update(_*srcObjs_, _**kwargs_)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.StopOrder.update "Link to this definition")
Update fields of the given `dataclass` object from zero or more `dataclass` source objects and/or from keyword arguments.

Return type:
[`object`](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)")

_class_ ib_async.order.StopLimitOrder(_action_, _totalQuantity_, _lmtPrice_, _stopPrice_, _**kwargs_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/order.html#StopLimitOrder)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.StopLimitOrder "Link to this definition")dict()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.StopLimitOrder.dict "Link to this definition")
Return dataclass values as `dict`. This is a non-recursive variant of `dataclasses.asdict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.StopLimitOrder.dict "ib_async.order.StopLimitOrder.dict")

nonDefaults()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.StopLimitOrder.nonDefaults "Link to this definition")
For a `dataclass` instance get the fields that are different from the default values and return as `dict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.StopLimitOrder.dict "ib_async.order.StopLimitOrder.dict")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)"), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")]

tuple()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.StopLimitOrder.tuple "Link to this definition")
Return dataclass values as `tuple`. This is a non-recursive variant of `dataclasses.astuple`.

Return type:
[`tuple`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.StopLimitOrder.tuple "ib_async.order.StopLimitOrder.tuple")[[`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)"), [`...`](https://docs.python.org/3/library/constants.html#Ellipsis "(in Python v3.14)")]

update(_*srcObjs_, _**kwargs_)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.StopLimitOrder.update "Link to this definition")
Update fields of the given `dataclass` object from zero or more `dataclass` source objects and/or from keyword arguments.

Return type:
[`object`](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)")

_class_ ib_async.order.OrderStatus(_orderId=0_, _status=''_, _filled=0.0_, _remaining=0.0_, _avgFillPrice=0.0_, _permId=0_, _parentId=0_, _lastFillPrice=0.0_, _clientId=0_, _whyHeld=''_, _mktCapPrice=0.0_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/order.html#OrderStatus)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderStatus "Link to this definition")orderId _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderStatus.orderId "Link to this definition")status _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderStatus.status "Link to this definition")filled _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=0.0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderStatus.filled "Link to this definition")remaining _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=0.0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderStatus.remaining "Link to this definition")avgFillPrice _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=0.0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderStatus.avgFillPrice "Link to this definition")permId _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderStatus.permId "Link to this definition")parentId _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderStatus.parentId "Link to this definition")lastFillPrice _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=0.0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderStatus.lastFillPrice "Link to this definition")clientId _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderStatus.clientId "Link to this definition")whyHeld _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderStatus.whyHeld "Link to this definition")mktCapPrice _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=0.0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderStatus.mktCapPrice "Link to this definition")_property_ total _:[float](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderStatus.total "Link to this definition")
Helper property to return the total size of this requested order.

PendingSubmit _:[`ClassVar`](https://docs.python.org/3/library/typing.html#typing.ClassVar "(in Python v3.14)")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")]_ _='PendingSubmit'_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderStatus.PendingSubmit "Link to this definition")PendingCancel _:[`ClassVar`](https://docs.python.org/3/library/typing.html#typing.ClassVar "(in Python v3.14)")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")]_ _='PendingCancel'_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderStatus.PendingCancel "Link to this definition")PreSubmitted _:[`ClassVar`](https://docs.python.org/3/library/typing.html#typing.ClassVar "(in Python v3.14)")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")]_ _='PreSubmitted'_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderStatus.PreSubmitted "Link to this definition")Submitted _:[`ClassVar`](https://docs.python.org/3/library/typing.html#typing.ClassVar "(in Python v3.14)")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")]_ _='Submitted'_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderStatus.Submitted "Link to this definition")ApiPending _:[`ClassVar`](https://docs.python.org/3/library/typing.html#typing.ClassVar "(in Python v3.14)")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")]_ _='ApiPending'_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderStatus.ApiPending "Link to this definition")ApiCancelled _:[`ClassVar`](https://docs.python.org/3/library/typing.html#typing.ClassVar "(in Python v3.14)")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")]_ _='ApiCancelled'_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderStatus.ApiCancelled "Link to this definition")ApiUpdate _:[`ClassVar`](https://docs.python.org/3/library/typing.html#typing.ClassVar "(in Python v3.14)")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")]_ _='ApiUpdate'_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderStatus.ApiUpdate "Link to this definition")Cancelled _:[`ClassVar`](https://docs.python.org/3/library/typing.html#typing.ClassVar "(in Python v3.14)")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")]_ _='Cancelled'_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderStatus.Cancelled "Link to this definition")Filled _:[`ClassVar`](https://docs.python.org/3/library/typing.html#typing.ClassVar "(in Python v3.14)")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")]_ _='Filled'_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderStatus.Filled "Link to this definition")Inactive _:[`ClassVar`](https://docs.python.org/3/library/typing.html#typing.ClassVar "(in Python v3.14)")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")]_ _='Inactive'_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderStatus.Inactive "Link to this definition")ValidationError _:[`ClassVar`](https://docs.python.org/3/library/typing.html#typing.ClassVar "(in Python v3.14)")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")]_ _='ValidationError'_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderStatus.ValidationError "Link to this definition")DoneStates _:[`ClassVar`](https://docs.python.org/3/library/typing.html#typing.ClassVar "(in Python v3.14)")[[`frozenset`](https://docs.python.org/3/library/stdtypes.html#frozenset "(in Python v3.14)")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")]]_ _=frozenset({'ApiCancelled','Cancelled','Filled','Inactive'})_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderStatus.DoneStates "Link to this definition")ActiveStates _:[`ClassVar`](https://docs.python.org/3/library/typing.html#typing.ClassVar "(in Python v3.14)")[[`frozenset`](https://docs.python.org/3/library/stdtypes.html#frozenset "(in Python v3.14)")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")]]_ _=frozenset({'ApiPending','ApiUpdate','PendingSubmit','PreSubmitted','Submitted','ValidationError'})_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderStatus.ActiveStates "Link to this definition")WaitingStates _:[`ClassVar`](https://docs.python.org/3/library/typing.html#typing.ClassVar "(in Python v3.14)")[[`frozenset`](https://docs.python.org/3/library/stdtypes.html#frozenset "(in Python v3.14)")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")]]_ _=frozenset({'ApiPending','PendingSubmit','PreSubmitted'})_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderStatus.WaitingStates "Link to this definition")WorkingStates _:[`ClassVar`](https://docs.python.org/3/library/typing.html#typing.ClassVar "(in Python v3.14)")[[`frozenset`](https://docs.python.org/3/library/stdtypes.html#frozenset "(in Python v3.14)")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")]]_ _=frozenset({'ApiUpdate','Submitted','ValidationError'})_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderStatus.WorkingStates "Link to this definition")dict()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderStatus.dict "Link to this definition")
Return dataclass values as `dict`. This is a non-recursive variant of `dataclasses.asdict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderStatus.dict "ib_async.order.OrderStatus.dict")

nonDefaults()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderStatus.nonDefaults "Link to this definition")
For a `dataclass` instance get the fields that are different from the default values and return as `dict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderStatus.dict "ib_async.order.OrderStatus.dict")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)"), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")]

tuple()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderStatus.tuple "Link to this definition")
Return dataclass values as `tuple`. This is a non-recursive variant of `dataclasses.astuple`.

Return type:
[`tuple`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderStatus.tuple "ib_async.order.OrderStatus.tuple")[[`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)"), [`...`](https://docs.python.org/3/library/constants.html#Ellipsis "(in Python v3.14)")]

update(_*srcObjs_, _**kwargs_)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderStatus.update "Link to this definition")
Update fields of the given `dataclass` object from zero or more `dataclass` source objects and/or from keyword arguments.

Return type:
[`object`](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)")

_class_ ib_async.order.OrderState(_status=''_, _initMarginBefore=''_, _maintMarginBefore=''_, _equityWithLoanBefore=''_, _initMarginChange=''_, _maintMarginChange=''_, _equityWithLoanChange=''_, _initMarginAfter=''_, _maintMarginAfter=''_, _equityWithLoanAfter=''_, _commission=1.7976931348623157e+308_, _minCommission=1.7976931348623157e+308_, _maxCommission=1.7976931348623157e+308_, _commissionCurrency=''_, _warningText=''_, _completedTime=''_, _completedStatus=''_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/order.html#OrderState)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderState "Link to this definition")status _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderState.status "Link to this definition")initMarginBefore _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderState.initMarginBefore "Link to this definition")maintMarginBefore _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderState.maintMarginBefore "Link to this definition")equityWithLoanBefore _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderState.equityWithLoanBefore "Link to this definition")initMarginChange _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderState.initMarginChange "Link to this definition")maintMarginChange _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderState.maintMarginChange "Link to this definition")equityWithLoanChange _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderState.equityWithLoanChange "Link to this definition")initMarginAfter _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderState.initMarginAfter "Link to this definition")maintMarginAfter _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderState.maintMarginAfter "Link to this definition")equityWithLoanAfter _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderState.equityWithLoanAfter "Link to this definition")commission _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=1.7976931348623157e+308_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderState.commission "Link to this definition")minCommission _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=1.7976931348623157e+308_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderState.minCommission "Link to this definition")maxCommission _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=1.7976931348623157e+308_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderState.maxCommission "Link to this definition")commissionCurrency _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderState.commissionCurrency "Link to this definition")warningText _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderState.warningText "Link to this definition")completedTime _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderState.completedTime "Link to this definition")completedStatus _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderState.completedStatus "Link to this definition")transform(_transformer_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/order.html#OrderState.transform)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderState.transform "Link to this definition")
Convert the numeric values of this OrderState into a new OrderState transformed by ‘using’

numeric(_digits=2_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/order.html#OrderState.numeric)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderState.numeric "Link to this definition")
Return a new OrderState with the current values values to floats instead of strings as returned from IBKR directly.

Return type:
[`OrderStateNumeric`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderStateNumeric "ib_async.order.OrderStateNumeric")

formatted(_digits=2_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/order.html#OrderState.formatted)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderState.formatted "Link to this definition")
Return a new OrderState with the current values as formatted strings.

dict()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderState.dict "Link to this definition")
Return dataclass values as `dict`. This is a non-recursive variant of `dataclasses.asdict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderState.dict "ib_async.order.OrderState.dict")

nonDefaults()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderState.nonDefaults "Link to this definition")
For a `dataclass` instance get the fields that are different from the default values and return as `dict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderState.dict "ib_async.order.OrderState.dict")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)"), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")]

tuple()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderState.tuple "Link to this definition")
Return dataclass values as `tuple`. This is a non-recursive variant of `dataclasses.astuple`.

Return type:
[`tuple`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderState.tuple "ib_async.order.OrderState.tuple")[[`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)"), [`...`](https://docs.python.org/3/library/constants.html#Ellipsis "(in Python v3.14)")]

update(_*srcObjs_, _**kwargs_)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderState.update "Link to this definition")
Update fields of the given `dataclass` object from zero or more `dataclass` source objects and/or from keyword arguments.

Return type:
[`object`](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)")

_class_ ib_async.order.OrderStateNumeric(_status=''_, _initMarginBefore=nan_, _maintMarginBefore=nan_, _equityWithLoanBefore=nan_, _initMarginChange=nan_, _maintMarginChange=nan_, _equityWithLoanChange=nan_, _initMarginAfter=nan_, _maintMarginAfter=nan_, _equityWithLoanAfter=nan_, _commission=1.7976931348623157e+308_, _minCommission=1.7976931348623157e+308_, _maxCommission=1.7976931348623157e+308_, _commissionCurrency=''_, _warningText=''_, _completedTime=''_, _completedStatus=''_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/order.html#OrderStateNumeric)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderStateNumeric "Link to this definition")
Just a type helper for mypy to check against if you convert OrderState to .numeric().

Usage:

state_numeric: OrderStateNumeric = state.numeric(digits=2)

initMarginBefore _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderStateNumeric.initMarginBefore "Link to this definition")maintMarginBefore _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderStateNumeric.maintMarginBefore "Link to this definition")equityWithLoanBefore _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderStateNumeric.equityWithLoanBefore "Link to this definition")initMarginChange _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderStateNumeric.initMarginChange "Link to this definition")maintMarginChange _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderStateNumeric.maintMarginChange "Link to this definition")equityWithLoanChange _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderStateNumeric.equityWithLoanChange "Link to this definition")initMarginAfter _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderStateNumeric.initMarginAfter "Link to this definition")maintMarginAfter _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderStateNumeric.maintMarginAfter "Link to this definition")equityWithLoanAfter _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderStateNumeric.equityWithLoanAfter "Link to this definition")dict()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderStateNumeric.dict "Link to this definition")
Return dataclass values as `dict`. This is a non-recursive variant of `dataclasses.asdict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderStateNumeric.dict "ib_async.order.OrderStateNumeric.dict")

nonDefaults()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderStateNumeric.nonDefaults "Link to this definition")
For a `dataclass` instance get the fields that are different from the default values and return as `dict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderStateNumeric.dict "ib_async.order.OrderStateNumeric.dict")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)"), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")]

tuple()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderStateNumeric.tuple "Link to this definition")
Return dataclass values as `tuple`. This is a non-recursive variant of `dataclasses.astuple`.

Return type:
[`tuple`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderStateNumeric.tuple "ib_async.order.OrderStateNumeric.tuple")[[`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)"), [`...`](https://docs.python.org/3/library/constants.html#Ellipsis "(in Python v3.14)")]

update(_*srcObjs_, _**kwargs_)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderStateNumeric.update "Link to this definition")
Update fields of the given `dataclass` object from zero or more `dataclass` source objects and/or from keyword arguments.

Return type:
[`object`](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)")

_class_ ib_async.order.OrderComboLeg(_price=1.7976931348623157e+308_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/order.html#OrderComboLeg)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderComboLeg "Link to this definition")price _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")|[`Decimal`](https://docs.python.org/3/library/decimal.html#decimal.Decimal "(in Python v3.14)")_ _=1.7976931348623157e+308_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderComboLeg.price "Link to this definition")dict()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderComboLeg.dict "Link to this definition")
Return dataclass values as `dict`. This is a non-recursive variant of `dataclasses.asdict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderComboLeg.dict "ib_async.order.OrderComboLeg.dict")

nonDefaults()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderComboLeg.nonDefaults "Link to this definition")
For a `dataclass` instance get the fields that are different from the default values and return as `dict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderComboLeg.dict "ib_async.order.OrderComboLeg.dict")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)"), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")]

tuple()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderComboLeg.tuple "Link to this definition")
Return dataclass values as `tuple`. This is a non-recursive variant of `dataclasses.astuple`.

Return type:
[`tuple`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderComboLeg.tuple "ib_async.order.OrderComboLeg.tuple")[[`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)"), [`...`](https://docs.python.org/3/library/constants.html#Ellipsis "(in Python v3.14)")]

update(_*srcObjs_, _**kwargs_)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderComboLeg.update "Link to this definition")
Update fields of the given `dataclass` object from zero or more `dataclass` source objects and/or from keyword arguments.

Return type:
[`object`](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)")

_class_ ib_async.order.Trade(_contract=<factory>_, _order=<factory>_, _orderStatus=<factory>_, _fills=<factory>_, _log=<factory>_, _advancedError=''_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/order.html#Trade)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Trade "Link to this definition")
Trade keeps track of an order, its status and all its fills.

Events:
*   `statusEvent` (trade: [`Trade`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Trade "ib_async.order.Trade"))

*   `modifyEvent` (trade: [`Trade`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Trade "ib_async.order.Trade"))

*   `fillEvent` (trade: [`Trade`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Trade "ib_async.order.Trade"), fill: [`Fill`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.Fill "ib_async.objects.Fill"))

*   `commissionReportEvent` (trade: [`Trade`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Trade "ib_async.order.Trade"), fill: [`Fill`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.Fill "ib_async.objects.Fill"), commissionReport: [`CommissionReport`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.CommissionReport "ib_async.objects.CommissionReport"))

*   `filledEvent` (trade: [`Trade`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Trade "ib_async.order.Trade"))

*   `cancelEvent` (trade: [`Trade`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Trade "ib_async.order.Trade"))

*   `cancelledEvent` (trade: [`Trade`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Trade "ib_async.order.Trade"))

contract _:[`Contract`](https://ib-api-reloaded.github.io/ib\_async/api.html#ib\_async.contract.Contract "ib\_async.contract.Contract")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Trade.contract "Link to this definition")order _:[`Order`](https://ib-api-reloaded.github.io/ib\_async/api.html#ib\_async.order.Order "ib\_async.order.Order")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Trade.order "Link to this definition")orderStatus _:[`OrderStatus`](https://ib-api-reloaded.github.io/ib\_async/api.html#ib\_async.order.OrderStatus "ib\_async.order.OrderStatus")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Trade.orderStatus "Link to this definition")fills _:[`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`Fill`](https://ib-api-reloaded.github.io/ib\_async/api.html#ib\_async.objects.Fill "ib\_async.objects.Fill")]_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Trade.fills "Link to this definition")log _:[`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`TradeLogEntry`](https://ib-api-reloaded.github.io/ib\_async/api.html#ib\_async.objects.TradeLogEntry "ib\_async.objects.TradeLogEntry")]_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Trade.log "Link to this definition")advancedError _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Trade.advancedError "Link to this definition")events _:[`ClassVar`](https://docs.python.org/3/library/typing.html#typing.ClassVar "(in Python v3.14)")_ _=('statusEvent','modifyEvent','fillEvent','commissionReportEvent','filledEvent','cancelEvent','cancelledEvent')_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Trade.events "Link to this definition")isWaiting()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/order.html#Trade.isWaiting)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Trade.isWaiting "Link to this definition")
True if sent to IBKR but not “Submitted” for live execution yet.

Return type:
[`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")

isWorking()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/order.html#Trade.isWorking)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Trade.isWorking "Link to this definition")
True if sent to IBKR but not “Submitted” for live execution yet.

Return type:
[`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")

isActive()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/order.html#Trade.isActive)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Trade.isActive "Link to this definition")
True if eligible for execution, false otherwise.

Return type:
[`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")

isDone()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/order.html#Trade.isDone)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Trade.isDone "Link to this definition")
True if completely filled or cancelled, false otherwise.

Return type:
[`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")

filled()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/order.html#Trade.filled)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Trade.filled "Link to this definition")
Number of shares filled.

Return type:
[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")

remaining()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/order.html#Trade.remaining)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Trade.remaining "Link to this definition")
Number of shares remaining to be filled.

Return type:
[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")

dict()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Trade.dict "Link to this definition")
Return dataclass values as `dict`. This is a non-recursive variant of `dataclasses.asdict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Trade.dict "ib_async.order.Trade.dict")

nonDefaults()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Trade.nonDefaults "Link to this definition")
For a `dataclass` instance get the fields that are different from the default values and return as `dict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Trade.dict "ib_async.order.Trade.dict")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)"), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")]

tuple()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Trade.tuple "Link to this definition")
Return dataclass values as `tuple`. This is a non-recursive variant of `dataclasses.astuple`.

Return type:
[`tuple`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Trade.tuple "ib_async.order.Trade.tuple")[[`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)"), [`...`](https://docs.python.org/3/library/constants.html#Ellipsis "(in Python v3.14)")]

update(_*srcObjs_, _**kwargs_)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.Trade.update "Link to this definition")
Update fields of the given `dataclass` object from zero or more `dataclass` source objects and/or from keyword arguments.

Return type:
[`object`](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)")

_class_ ib_async.order.BracketOrder(_parent_, _takeProfit_, _stopLoss_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/order.html#BracketOrder)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.BracketOrder "Link to this definition")
Create new instance of BracketOrder(parent, takeProfit, stopLoss)

parent _:[`Order`](https://ib-api-reloaded.github.io/ib\_async/api.html#ib\_async.order.Order "ib\_async.order.Order")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.BracketOrder.parent "Link to this definition")takeProfit _:[`Order`](https://ib-api-reloaded.github.io/ib\_async/api.html#ib\_async.order.Order "ib\_async.order.Order")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.BracketOrder.takeProfit "Link to this definition")stopLoss _:[`Order`](https://ib-api-reloaded.github.io/ib\_async/api.html#ib\_async.order.Order "ib\_async.order.Order")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.BracketOrder.stopLoss "Link to this definition")_class_ ib_async.order.OrderCondition[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/order.html#OrderCondition)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderCondition "Link to this definition")_static_ createClass(_condType_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/order.html#OrderCondition.createClass)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderCondition.createClass "Link to this definition")And()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/order.html#OrderCondition.And)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderCondition.And "Link to this definition")Or()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/order.html#OrderCondition.Or)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderCondition.Or "Link to this definition")dict()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderCondition.dict "Link to this definition")
Return dataclass values as `dict`. This is a non-recursive variant of `dataclasses.asdict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderCondition.dict "ib_async.order.OrderCondition.dict")

nonDefaults()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderCondition.nonDefaults "Link to this definition")
For a `dataclass` instance get the fields that are different from the default values and return as `dict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderCondition.dict "ib_async.order.OrderCondition.dict")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)"), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")]

tuple()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderCondition.tuple "Link to this definition")
Return dataclass values as `tuple`. This is a non-recursive variant of `dataclasses.astuple`.

Return type:
[`tuple`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderCondition.tuple "ib_async.order.OrderCondition.tuple")[[`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)"), [`...`](https://docs.python.org/3/library/constants.html#Ellipsis "(in Python v3.14)")]

update(_*srcObjs_, _**kwargs_)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.OrderCondition.update "Link to this definition")
Update fields of the given `dataclass` object from zero or more `dataclass` source objects and/or from keyword arguments.

Return type:
[`object`](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)")

_class_ ib_async.order.PriceCondition(_condType=1_, _conjunction='a'_, _isMore=True_, _price=0.0_, _conId=0_, _exch=''_, _triggerMethod=0_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/order.html#PriceCondition)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.PriceCondition "Link to this definition")condType _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=1_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.PriceCondition.condType "Link to this definition")conjunction _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _='a'_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.PriceCondition.conjunction "Link to this definition")isMore _:[`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")_ _=True_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.PriceCondition.isMore "Link to this definition")price _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=0.0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.PriceCondition.price "Link to this definition")conId _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.PriceCondition.conId "Link to this definition")exch _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.PriceCondition.exch "Link to this definition")triggerMethod _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.PriceCondition.triggerMethod "Link to this definition")dict()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.PriceCondition.dict "Link to this definition")
Return dataclass values as `dict`. This is a non-recursive variant of `dataclasses.asdict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.PriceCondition.dict "ib_async.order.PriceCondition.dict")

nonDefaults()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.PriceCondition.nonDefaults "Link to this definition")
For a `dataclass` instance get the fields that are different from the default values and return as `dict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.PriceCondition.dict "ib_async.order.PriceCondition.dict")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)"), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")]

tuple()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.PriceCondition.tuple "Link to this definition")
Return dataclass values as `tuple`. This is a non-recursive variant of `dataclasses.astuple`.

Return type:
[`tuple`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.PriceCondition.tuple "ib_async.order.PriceCondition.tuple")[[`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)"), [`...`](https://docs.python.org/3/library/constants.html#Ellipsis "(in Python v3.14)")]

update(_*srcObjs_, _**kwargs_)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.PriceCondition.update "Link to this definition")
Update fields of the given `dataclass` object from zero or more `dataclass` source objects and/or from keyword arguments.

Return type:
[`object`](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)")

_class_ ib_async.order.TimeCondition(_condType=3_, _conjunction='a'_, _isMore=True_, _time=''_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/order.html#TimeCondition)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.TimeCondition "Link to this definition")condType _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=3_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.TimeCondition.condType "Link to this definition")conjunction _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _='a'_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.TimeCondition.conjunction "Link to this definition")isMore _:[`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")_ _=True_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.TimeCondition.isMore "Link to this definition")time _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.TimeCondition.time "Link to this definition")dict()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.TimeCondition.dict "Link to this definition")
Return dataclass values as `dict`. This is a non-recursive variant of `dataclasses.asdict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.TimeCondition.dict "ib_async.order.TimeCondition.dict")

nonDefaults()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.TimeCondition.nonDefaults "Link to this definition")
For a `dataclass` instance get the fields that are different from the default values and return as `dict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.TimeCondition.dict "ib_async.order.TimeCondition.dict")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)"), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")]

tuple()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.TimeCondition.tuple "Link to this definition")
Return dataclass values as `tuple`. This is a non-recursive variant of `dataclasses.astuple`.

Return type:
[`tuple`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.TimeCondition.tuple "ib_async.order.TimeCondition.tuple")[[`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)"), [`...`](https://docs.python.org/3/library/constants.html#Ellipsis "(in Python v3.14)")]

update(_*srcObjs_, _**kwargs_)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.TimeCondition.update "Link to this definition")
Update fields of the given `dataclass` object from zero or more `dataclass` source objects and/or from keyword arguments.

Return type:
[`object`](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)")

_class_ ib_async.order.MarginCondition(_condType=4_, _conjunction='a'_, _isMore=True_, _percent=0_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/order.html#MarginCondition)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.MarginCondition "Link to this definition")condType _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=4_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.MarginCondition.condType "Link to this definition")conjunction _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _='a'_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.MarginCondition.conjunction "Link to this definition")isMore _:[`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")_ _=True_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.MarginCondition.isMore "Link to this definition")percent _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.MarginCondition.percent "Link to this definition")dict()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.MarginCondition.dict "Link to this definition")
Return dataclass values as `dict`. This is a non-recursive variant of `dataclasses.asdict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.MarginCondition.dict "ib_async.order.MarginCondition.dict")

nonDefaults()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.MarginCondition.nonDefaults "Link to this definition")
For a `dataclass` instance get the fields that are different from the default values and return as `dict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.MarginCondition.dict "ib_async.order.MarginCondition.dict")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)"), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")]

tuple()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.MarginCondition.tuple "Link to this definition")
Return dataclass values as `tuple`. This is a non-recursive variant of `dataclasses.astuple`.

Return type:
[`tuple`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.MarginCondition.tuple "ib_async.order.MarginCondition.tuple")[[`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)"), [`...`](https://docs.python.org/3/library/constants.html#Ellipsis "(in Python v3.14)")]

update(_*srcObjs_, _**kwargs_)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.MarginCondition.update "Link to this definition")
Update fields of the given `dataclass` object from zero or more `dataclass` source objects and/or from keyword arguments.

Return type:
[`object`](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)")

_class_ ib_async.order.ExecutionCondition(_condType=5_, _conjunction='a'_, _secType=''_, _exch=''_, _symbol=''_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/order.html#ExecutionCondition)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.ExecutionCondition "Link to this definition")condType _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=5_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.ExecutionCondition.condType "Link to this definition")conjunction _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _='a'_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.ExecutionCondition.conjunction "Link to this definition")secType _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.ExecutionCondition.secType "Link to this definition")exch _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.ExecutionCondition.exch "Link to this definition")symbol _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.ExecutionCondition.symbol "Link to this definition")dict()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.ExecutionCondition.dict "Link to this definition")
Return dataclass values as `dict`. This is a non-recursive variant of `dataclasses.asdict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.ExecutionCondition.dict "ib_async.order.ExecutionCondition.dict")

nonDefaults()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.ExecutionCondition.nonDefaults "Link to this definition")
For a `dataclass` instance get the fields that are different from the default values and return as `dict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.ExecutionCondition.dict "ib_async.order.ExecutionCondition.dict")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)"), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")]

tuple()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.ExecutionCondition.tuple "Link to this definition")
Return dataclass values as `tuple`. This is a non-recursive variant of `dataclasses.astuple`.

Return type:
[`tuple`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.ExecutionCondition.tuple "ib_async.order.ExecutionCondition.tuple")[[`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)"), [`...`](https://docs.python.org/3/library/constants.html#Ellipsis "(in Python v3.14)")]

update(_*srcObjs_, _**kwargs_)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.ExecutionCondition.update "Link to this definition")
Update fields of the given `dataclass` object from zero or more `dataclass` source objects and/or from keyword arguments.

Return type:
[`object`](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)")

_class_ ib_async.order.VolumeCondition(_condType=6_, _conjunction='a'_, _isMore=True_, _volume=0_, _conId=0_, _exch=''_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/order.html#VolumeCondition)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.VolumeCondition "Link to this definition")condType _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=6_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.VolumeCondition.condType "Link to this definition")conjunction _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _='a'_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.VolumeCondition.conjunction "Link to this definition")isMore _:[`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")_ _=True_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.VolumeCondition.isMore "Link to this definition")volume _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.VolumeCondition.volume "Link to this definition")conId _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.VolumeCondition.conId "Link to this definition")exch _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.VolumeCondition.exch "Link to this definition")dict()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.VolumeCondition.dict "Link to this definition")
Return dataclass values as `dict`. This is a non-recursive variant of `dataclasses.asdict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.VolumeCondition.dict "ib_async.order.VolumeCondition.dict")

nonDefaults()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.VolumeCondition.nonDefaults "Link to this definition")
For a `dataclass` instance get the fields that are different from the default values and return as `dict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.VolumeCondition.dict "ib_async.order.VolumeCondition.dict")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)"), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")]

tuple()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.VolumeCondition.tuple "Link to this definition")
Return dataclass values as `tuple`. This is a non-recursive variant of `dataclasses.astuple`.

Return type:
[`tuple`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.VolumeCondition.tuple "ib_async.order.VolumeCondition.tuple")[[`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)"), [`...`](https://docs.python.org/3/library/constants.html#Ellipsis "(in Python v3.14)")]

update(_*srcObjs_, _**kwargs_)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.VolumeCondition.update "Link to this definition")
Update fields of the given `dataclass` object from zero or more `dataclass` source objects and/or from keyword arguments.

Return type:
[`object`](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)")

_class_ ib_async.order.PercentChangeCondition(_condType=7_, _conjunction='a'_, _isMore=True_, _changePercent=0.0_, _conId=0_, _exch=''_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/order.html#PercentChangeCondition)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.PercentChangeCondition "Link to this definition")condType _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=7_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.PercentChangeCondition.condType "Link to this definition")conjunction _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _='a'_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.PercentChangeCondition.conjunction "Link to this definition")isMore _:[`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")_ _=True_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.PercentChangeCondition.isMore "Link to this definition")changePercent _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=0.0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.PercentChangeCondition.changePercent "Link to this definition")conId _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.PercentChangeCondition.conId "Link to this definition")exch _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.PercentChangeCondition.exch "Link to this definition")dict()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.PercentChangeCondition.dict "Link to this definition")
Return dataclass values as `dict`. This is a non-recursive variant of `dataclasses.asdict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.PercentChangeCondition.dict "ib_async.order.PercentChangeCondition.dict")

nonDefaults()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.PercentChangeCondition.nonDefaults "Link to this definition")
For a `dataclass` instance get the fields that are different from the default values and return as `dict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.PercentChangeCondition.dict "ib_async.order.PercentChangeCondition.dict")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)"), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")]

tuple()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.PercentChangeCondition.tuple "Link to this definition")
Return dataclass values as `tuple`. This is a non-recursive variant of `dataclasses.astuple`.

Return type:
[`tuple`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.PercentChangeCondition.tuple "ib_async.order.PercentChangeCondition.tuple")[[`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)"), [`...`](https://docs.python.org/3/library/constants.html#Ellipsis "(in Python v3.14)")]

update(_*srcObjs_, _**kwargs_)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.order.PercentChangeCondition.update "Link to this definition")
Update fields of the given `dataclass` object from zero or more `dataclass` source objects and/or from keyword arguments.

Return type:
[`object`](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)")

Contract[](https://ib-api-reloaded.github.io/ib_async/api.html#module-ib_async.contract "Link to this heading")
----------------------------------------------------------------------------------------------------------------

Financial instrument types used by Interactive Brokers.

_class_ ib_async.contract.Contract(_secType=''_, _conId=0_, _symbol=''_, _lastTradeDateOrContractMonth=''_, _strike=0.0_, _right=''_, _multiplier=''_, _exchange=''_, _primaryExchange=''_, _currency=''_, _localSymbol=''_, _tradingClass=''_, _includeExpired=False_, _secIdType=''_, _secId=''_, _description=''_, _issuerId=''_, _comboLegsDescrip=''_, _comboLegs=<factory>_, _deltaNeutralContract=None_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/contract.html#Contract)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Contract "Link to this definition")
`Contract(**kwargs)` can create any contract using keyword arguments. To simplify working with contracts, there are also more specialized contracts that take optional positional arguments. Some examples:

Contract(conId=270639)
Stock('AMD', 'SMART', 'USD')
Stock('INTC', 'SMART', 'USD', primaryExchange='NASDAQ')
Forex('EURUSD')
CFD('IBUS30')
Future('ES', '20180921', 'GLOBEX')
Option('SPY', '20170721', 240, 'C', 'SMART')
Bond(secIdType='ISIN', secId='US03076KAA60')
Crypto('BTC', 'PAXOS', 'USD')

Parameters:
*   **conId** ([_int_](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) – The unique IB contract identifier.

*   **symbol** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – The contract (or its underlying) symbol.

*   **secType** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) –

The security type:

    *   ’STK’ = Stock (or ETF)

    *   ’OPT’ = Option

    *   ’FUT’ = Future

    *   ’IND’ = Index

    *   ’FOP’ = Futures option

    *   ’CASH’ = Forex pair

    *   ’CFD’ = CFD

    *   ’BAG’ = Combo

    *   ’WAR’ = Warrant

    *   ’BOND’ = Bond

    *   ’CMDTY’ = Commodity

    *   ’NEWS’ = News

    *   ’FUND’ = Mutual fund

    *   ’CRYPTO’ = Crypto currency

    *   ’EVENT’ = Bet on an event

*   **lastTradeDateOrContractMonth** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – The contract’s last trading day or contract month (for Options and Futures). Strings with format YYYYMM will be interpreted as the Contract Month whereas YYYYMMDD will be interpreted as Last Trading Day.

*   **strike** ([_float_](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")) – The option’s strike price.

*   **right** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – Put or Call. Valid values are ‘P’, ‘PUT’, ‘C’, ‘CALL’, or ‘’ for non-options.

*   **multiplier** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – The instrument’s multiplier (i.e. options, futures).

*   **exchange** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – The destination exchange.

*   **currency** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – The underlying’s currency.

*   **localSymbol** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – The contract’s symbol within its primary exchange. For options, this will be the OCC symbol.

*   **primaryExchange** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – The contract’s primary exchange. For smart routed contracts, used to define contract in case of ambiguity. Should be defined as native exchange of contract, e.g. ISLAND for MSFT. For exchanges which contain a period in name, will only be part of exchange name prior to period, i.e. ENEXT for ENEXT.BE.

*   **tradingClass** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – The trading class name for this contract. Available in TWS contract description window as well. For example, GBL Dec ‘13 future’s trading class is “FGBL”.

*   **includeExpired** ([_bool_](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")) – If set to true, contract details requests and historical data queries can be performed pertaining to expired futures contracts. Expired options or other instrument types are not available.

*   **secIdType** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) –

Security identifier type. Examples for Apple:

    *   secIdType=’ISIN’, secId=’US0378331005’

    *   secIdType=’CUSIP’, secId=’037833100’

*   **secId** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – Security identifier.

*   **comboLegsDescription** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – Description of the combo legs.

*   **comboLegs** (_List_ _[_[_ComboLeg_](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ComboLeg "ib_async.contract.ComboLeg")_]_) – The legs of a combined contract definition.

*   **deltaNeutralContract** ([_DeltaNeutralContract_](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.DeltaNeutralContract "ib_async.contract.DeltaNeutralContract")) – Delta and underlying price for Delta-Neutral combo orders.

secType _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Contract.secType "Link to this definition")conId _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Contract.conId "Link to this definition")symbol _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Contract.symbol "Link to this definition")lastTradeDateOrContractMonth _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Contract.lastTradeDateOrContractMonth "Link to this definition")strike _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=0.0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Contract.strike "Link to this definition")right _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Contract.right "Link to this definition")multiplier _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Contract.multiplier "Link to this definition")exchange _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Contract.exchange "Link to this definition")primaryExchange _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Contract.primaryExchange "Link to this definition")currency _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Contract.currency "Link to this definition")localSymbol _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Contract.localSymbol "Link to this definition")tradingClass _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Contract.tradingClass "Link to this definition")includeExpired _:[`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")_ _=False_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Contract.includeExpired "Link to this definition")secIdType _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Contract.secIdType "Link to this definition")secId _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Contract.secId "Link to this definition")description _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Contract.description "Link to this definition")issuerId _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Contract.issuerId "Link to this definition")comboLegsDescrip _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Contract.comboLegsDescrip "Link to this definition")comboLegs _:[`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`ComboLeg`](https://ib-api-reloaded.github.io/ib\_async/api.html#ib\_async.contract.ComboLeg "ib\_async.contract.ComboLeg")]_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Contract.comboLegs "Link to this definition")deltaNeutralContract _:[`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional "(in Python v3.14)")[[`DeltaNeutralContract`](https://ib-api-reloaded.github.io/ib\_async/api.html#ib\_async.contract.DeltaNeutralContract "ib\_async.contract.DeltaNeutralContract")]_ _=None_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Contract.deltaNeutralContract "Link to this definition")_static_ create(_**kwargs_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/contract.html#Contract.create)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Contract.create "Link to this definition")
Create and a return a specialized contract based on the given secType, or a general Contract if secType is not given.

Return type:
[`Contract`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Contract "ib_async.contract.Contract")

_static_ recreate(_c_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/contract.html#Contract.recreate)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Contract.recreate "Link to this definition")
Comply an existing generic Contract into its most specific type.

Return type:
[`Contract`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Contract "ib_async.contract.Contract")

isHashable()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/contract.html#Contract.isHashable)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Contract.isHashable "Link to this definition")
See if this contract can be hashed by conId.

Return type:
[`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")

Note: Bag contracts always get conId=28812380, so they’re not hashable by conId,
but we generate a synthetic hash for them based on leg details instead.

dict()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Contract.dict "Link to this definition")
Return dataclass values as `dict`. This is a non-recursive variant of `dataclasses.asdict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Contract.dict "ib_async.contract.Contract.dict")

nonDefaults()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Contract.nonDefaults "Link to this definition")
For a `dataclass` instance get the fields that are different from the default values and return as `dict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Contract.dict "ib_async.contract.Contract.dict")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)"), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")]

tuple()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Contract.tuple "Link to this definition")
Return dataclass values as `tuple`. This is a non-recursive variant of `dataclasses.astuple`.

Return type:
[`tuple`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Contract.tuple "ib_async.contract.Contract.tuple")[[`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)"), [`...`](https://docs.python.org/3/library/constants.html#Ellipsis "(in Python v3.14)")]

update(_*srcObjs_, _**kwargs_)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Contract.update "Link to this definition")
Update fields of the given `dataclass` object from zero or more `dataclass` source objects and/or from keyword arguments.

Return type:
[`object`](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)")

_class_ ib_async.contract.Stock(_symbol=''_, _exchange=''_, _currency=''_, _**kwargs_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/contract.html#Stock)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Stock "Link to this definition")
Stock contract.

Parameters:
*   **symbol** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – Symbol name.

*   **exchange** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – Destination exchange.

*   **currency** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – Underlying currency.

dict()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Stock.dict "Link to this definition")
Return dataclass values as `dict`. This is a non-recursive variant of `dataclasses.asdict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Stock.dict "ib_async.contract.Stock.dict")

nonDefaults()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Stock.nonDefaults "Link to this definition")
For a `dataclass` instance get the fields that are different from the default values and return as `dict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Stock.dict "ib_async.contract.Stock.dict")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)"), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")]

tuple()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Stock.tuple "Link to this definition")
Return dataclass values as `tuple`. This is a non-recursive variant of `dataclasses.astuple`.

Return type:
[`tuple`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Stock.tuple "ib_async.contract.Stock.tuple")[[`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)"), [`...`](https://docs.python.org/3/library/constants.html#Ellipsis "(in Python v3.14)")]

update(_*srcObjs_, _**kwargs_)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Stock.update "Link to this definition")
Update fields of the given `dataclass` object from zero or more `dataclass` source objects and/or from keyword arguments.

Return type:
[`object`](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)")

_class_ ib_async.contract.Option(_symbol=''_, _lastTradeDateOrContractMonth=''_, _strike=0.0_, _right=''_, _exchange=''_, _multiplier=''_, _currency=''_, _**kwargs_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/contract.html#Option)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Option "Link to this definition")
Option contract.

Parameters:
*   **symbol** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – Symbol name.

*   **lastTradeDateOrContractMonth** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) –

The option’s last trading day or contract month.

    *   YYYYMM format: To specify last month

    *   YYYYMMDD format: To specify last trading day

*   **strike** ([`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")) – The option’s strike price.

*   **right** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – Put or call option. Valid values are ‘P’, ‘PUT’, ‘C’ or ‘CALL’.

*   **exchange** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – Destination exchange.

*   **multiplier** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – The contract multiplier.

*   **currency** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – Underlying currency.

dict()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Option.dict "Link to this definition")
Return dataclass values as `dict`. This is a non-recursive variant of `dataclasses.asdict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Option.dict "ib_async.contract.Option.dict")

nonDefaults()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Option.nonDefaults "Link to this definition")
For a `dataclass` instance get the fields that are different from the default values and return as `dict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Option.dict "ib_async.contract.Option.dict")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)"), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")]

tuple()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Option.tuple "Link to this definition")
Return dataclass values as `tuple`. This is a non-recursive variant of `dataclasses.astuple`.

Return type:
[`tuple`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Option.tuple "ib_async.contract.Option.tuple")[[`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)"), [`...`](https://docs.python.org/3/library/constants.html#Ellipsis "(in Python v3.14)")]

update(_*srcObjs_, _**kwargs_)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Option.update "Link to this definition")
Update fields of the given `dataclass` object from zero or more `dataclass` source objects and/or from keyword arguments.

Return type:
[`object`](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)")

_class_ ib_async.contract.Future(_symbol=''_, _lastTradeDateOrContractMonth=''_, _exchange=''_, _localSymbol=''_, _multiplier=''_, _currency=''_, _**kwargs_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/contract.html#Future)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Future "Link to this definition")
Future contract.

Parameters:
*   **symbol** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – Symbol name.

*   **lastTradeDateOrContractMonth** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) –

The option’s last trading day or contract month.

    *   YYYYMM format: To specify last month

    *   YYYYMMDD format: To specify last trading day

*   **exchange** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – Destination exchange.

*   **localSymbol** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – The contract’s symbol within its primary exchange.

*   **multiplier** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – The contract multiplier.

*   **currency** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – Underlying currency.

dict()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Future.dict "Link to this definition")
Return dataclass values as `dict`. This is a non-recursive variant of `dataclasses.asdict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Future.dict "ib_async.contract.Future.dict")

nonDefaults()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Future.nonDefaults "Link to this definition")
For a `dataclass` instance get the fields that are different from the default values and return as `dict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Future.dict "ib_async.contract.Future.dict")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)"), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")]

tuple()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Future.tuple "Link to this definition")
Return dataclass values as `tuple`. This is a non-recursive variant of `dataclasses.astuple`.

Return type:
[`tuple`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Future.tuple "ib_async.contract.Future.tuple")[[`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)"), [`...`](https://docs.python.org/3/library/constants.html#Ellipsis "(in Python v3.14)")]

update(_*srcObjs_, _**kwargs_)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Future.update "Link to this definition")
Update fields of the given `dataclass` object from zero or more `dataclass` source objects and/or from keyword arguments.

Return type:
[`object`](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)")

_class_ ib_async.contract.ContFuture(_symbol=''_, _exchange=''_, _localSymbol=''_, _multiplier=''_, _currency=''_, _**kwargs_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/contract.html#ContFuture)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ContFuture "Link to this definition")
Continuous future contract.

Parameters:
*   **symbol** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – Symbol name.

*   **exchange** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – Destination exchange.

*   **localSymbol** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – The contract’s symbol within its primary exchange.

*   **multiplier** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – The contract multiplier.

*   **currency** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – Underlying currency.

dict()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ContFuture.dict "Link to this definition")
Return dataclass values as `dict`. This is a non-recursive variant of `dataclasses.asdict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ContFuture.dict "ib_async.contract.ContFuture.dict")

nonDefaults()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ContFuture.nonDefaults "Link to this definition")
For a `dataclass` instance get the fields that are different from the default values and return as `dict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ContFuture.dict "ib_async.contract.ContFuture.dict")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)"), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")]

tuple()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ContFuture.tuple "Link to this definition")
Return dataclass values as `tuple`. This is a non-recursive variant of `dataclasses.astuple`.

Return type:
[`tuple`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ContFuture.tuple "ib_async.contract.ContFuture.tuple")[[`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)"), [`...`](https://docs.python.org/3/library/constants.html#Ellipsis "(in Python v3.14)")]

update(_*srcObjs_, _**kwargs_)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ContFuture.update "Link to this definition")
Update fields of the given `dataclass` object from zero or more `dataclass` source objects and/or from keyword arguments.

Return type:
[`object`](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)")

_class_ ib_async.contract.Forex(_pair=''_, _exchange='IDEALPRO'_, _symbol=''_, _currency=''_, _**kwargs_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/contract.html#Forex)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Forex "Link to this definition")
Foreign exchange currency pair.

Parameters:
*   **pair** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – Shortcut for specifying symbol and currency, like ‘EURUSD’.

*   **exchange** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – Destination exchange.

*   **symbol** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – Base currency.

*   **currency** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – Quote currency.

pair()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/contract.html#Forex.pair)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Forex.pair "Link to this definition")
Short name of pair.

Return type:
[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")

dict()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Forex.dict "Link to this definition")
Return dataclass values as `dict`. This is a non-recursive variant of `dataclasses.asdict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Forex.dict "ib_async.contract.Forex.dict")

nonDefaults()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Forex.nonDefaults "Link to this definition")
For a `dataclass` instance get the fields that are different from the default values and return as `dict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Forex.dict "ib_async.contract.Forex.dict")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)"), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")]

tuple()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Forex.tuple "Link to this definition")
Return dataclass values as `tuple`. This is a non-recursive variant of `dataclasses.astuple`.

Return type:
[`tuple`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Forex.tuple "ib_async.contract.Forex.tuple")[[`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)"), [`...`](https://docs.python.org/3/library/constants.html#Ellipsis "(in Python v3.14)")]

update(_*srcObjs_, _**kwargs_)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Forex.update "Link to this definition")
Update fields of the given `dataclass` object from zero or more `dataclass` source objects and/or from keyword arguments.

Return type:
[`object`](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)")

_class_ ib_async.contract.Index(_symbol=''_, _exchange=''_, _currency=''_, _**kwargs_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/contract.html#Index)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Index "Link to this definition")
Index.

Parameters:
*   **symbol** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – Symbol name.

*   **exchange** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – Destination exchange.

*   **currency** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – Underlying currency.

dict()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Index.dict "Link to this definition")
Return dataclass values as `dict`. This is a non-recursive variant of `dataclasses.asdict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Index.dict "ib_async.contract.Index.dict")

nonDefaults()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Index.nonDefaults "Link to this definition")
For a `dataclass` instance get the fields that are different from the default values and return as `dict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Index.dict "ib_async.contract.Index.dict")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)"), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")]

tuple()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Index.tuple "Link to this definition")
Return dataclass values as `tuple`. This is a non-recursive variant of `dataclasses.astuple`.

Return type:
[`tuple`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Index.tuple "ib_async.contract.Index.tuple")[[`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)"), [`...`](https://docs.python.org/3/library/constants.html#Ellipsis "(in Python v3.14)")]

update(_*srcObjs_, _**kwargs_)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Index.update "Link to this definition")
Update fields of the given `dataclass` object from zero or more `dataclass` source objects and/or from keyword arguments.

Return type:
[`object`](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)")

_class_ ib_async.contract.CFD(_symbol=''_, _exchange=''_, _currency=''_, _**kwargs_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/contract.html#CFD)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.CFD "Link to this definition")
Contract For Difference.

Parameters:
*   **symbol** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – Symbol name.

*   **exchange** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – Destination exchange.

*   **currency** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – Underlying currency.

dict()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.CFD.dict "Link to this definition")
Return dataclass values as `dict`. This is a non-recursive variant of `dataclasses.asdict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.CFD.dict "ib_async.contract.CFD.dict")

nonDefaults()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.CFD.nonDefaults "Link to this definition")
For a `dataclass` instance get the fields that are different from the default values and return as `dict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.CFD.dict "ib_async.contract.CFD.dict")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)"), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")]

tuple()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.CFD.tuple "Link to this definition")
Return dataclass values as `tuple`. This is a non-recursive variant of `dataclasses.astuple`.

Return type:
[`tuple`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.CFD.tuple "ib_async.contract.CFD.tuple")[[`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)"), [`...`](https://docs.python.org/3/library/constants.html#Ellipsis "(in Python v3.14)")]

update(_*srcObjs_, _**kwargs_)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.CFD.update "Link to this definition")
Update fields of the given `dataclass` object from zero or more `dataclass` source objects and/or from keyword arguments.

Return type:
[`object`](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)")

_class_ ib_async.contract.Commodity(_symbol=''_, _exchange=''_, _currency=''_, _**kwargs_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/contract.html#Commodity)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Commodity "Link to this definition")
Commodity.

Parameters:
*   **symbol** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – Symbol name.

*   **exchange** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – Destination exchange.

*   **currency** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – Underlying currency.

dict()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Commodity.dict "Link to this definition")
Return dataclass values as `dict`. This is a non-recursive variant of `dataclasses.asdict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Commodity.dict "ib_async.contract.Commodity.dict")

nonDefaults()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Commodity.nonDefaults "Link to this definition")
For a `dataclass` instance get the fields that are different from the default values and return as `dict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Commodity.dict "ib_async.contract.Commodity.dict")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)"), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")]

tuple()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Commodity.tuple "Link to this definition")
Return dataclass values as `tuple`. This is a non-recursive variant of `dataclasses.astuple`.

Return type:
[`tuple`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Commodity.tuple "ib_async.contract.Commodity.tuple")[[`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)"), [`...`](https://docs.python.org/3/library/constants.html#Ellipsis "(in Python v3.14)")]

update(_*srcObjs_, _**kwargs_)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Commodity.update "Link to this definition")
Update fields of the given `dataclass` object from zero or more `dataclass` source objects and/or from keyword arguments.

Return type:
[`object`](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)")

_class_ ib_async.contract.Bond(_**kwargs_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/contract.html#Bond)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Bond "Link to this definition")
Bond.

dict()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Bond.dict "Link to this definition")
Return dataclass values as `dict`. This is a non-recursive variant of `dataclasses.asdict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Bond.dict "ib_async.contract.Bond.dict")

nonDefaults()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Bond.nonDefaults "Link to this definition")
For a `dataclass` instance get the fields that are different from the default values and return as `dict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Bond.dict "ib_async.contract.Bond.dict")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)"), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")]

tuple()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Bond.tuple "Link to this definition")
Return dataclass values as `tuple`. This is a non-recursive variant of `dataclasses.astuple`.

Return type:
[`tuple`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Bond.tuple "ib_async.contract.Bond.tuple")[[`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)"), [`...`](https://docs.python.org/3/library/constants.html#Ellipsis "(in Python v3.14)")]

update(_*srcObjs_, _**kwargs_)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Bond.update "Link to this definition")
Update fields of the given `dataclass` object from zero or more `dataclass` source objects and/or from keyword arguments.

Return type:
[`object`](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)")

_class_ ib_async.contract.FuturesOption(_symbol=''_, _lastTradeDateOrContractMonth=''_, _strike=0.0_, _right=''_, _exchange=''_, _multiplier=''_, _currency=''_, _**kwargs_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/contract.html#FuturesOption)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.FuturesOption "Link to this definition")
Option on a futures contract.

Parameters:
*   **symbol** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – Symbol name.

*   **lastTradeDateOrContractMonth** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) –

The option’s last trading day or contract month.

    *   YYYYMM format: To specify last month

    *   YYYYMMDD format: To specify last trading day

*   **strike** ([`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")) – The option’s strike price.

*   **right** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – Put or call option. Valid values are ‘P’, ‘PUT’, ‘C’ or ‘CALL’.

*   **exchange** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – Destination exchange.

*   **multiplier** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – The contract multiplier.

*   **currency** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – Underlying currency.

dict()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.FuturesOption.dict "Link to this definition")
Return dataclass values as `dict`. This is a non-recursive variant of `dataclasses.asdict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.FuturesOption.dict "ib_async.contract.FuturesOption.dict")

nonDefaults()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.FuturesOption.nonDefaults "Link to this definition")
For a `dataclass` instance get the fields that are different from the default values and return as `dict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.FuturesOption.dict "ib_async.contract.FuturesOption.dict")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)"), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")]

tuple()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.FuturesOption.tuple "Link to this definition")
Return dataclass values as `tuple`. This is a non-recursive variant of `dataclasses.astuple`.

Return type:
[`tuple`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.FuturesOption.tuple "ib_async.contract.FuturesOption.tuple")[[`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)"), [`...`](https://docs.python.org/3/library/constants.html#Ellipsis "(in Python v3.14)")]

update(_*srcObjs_, _**kwargs_)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.FuturesOption.update "Link to this definition")
Update fields of the given `dataclass` object from zero or more `dataclass` source objects and/or from keyword arguments.

Return type:
[`object`](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)")

_class_ ib_async.contract.MutualFund(_**kwargs_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/contract.html#MutualFund)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.MutualFund "Link to this definition")
Mutual fund.

dict()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.MutualFund.dict "Link to this definition")
Return dataclass values as `dict`. This is a non-recursive variant of `dataclasses.asdict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.MutualFund.dict "ib_async.contract.MutualFund.dict")

nonDefaults()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.MutualFund.nonDefaults "Link to this definition")
For a `dataclass` instance get the fields that are different from the default values and return as `dict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.MutualFund.dict "ib_async.contract.MutualFund.dict")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)"), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")]

tuple()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.MutualFund.tuple "Link to this definition")
Return dataclass values as `tuple`. This is a non-recursive variant of `dataclasses.astuple`.

Return type:
[`tuple`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.MutualFund.tuple "ib_async.contract.MutualFund.tuple")[[`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)"), [`...`](https://docs.python.org/3/library/constants.html#Ellipsis "(in Python v3.14)")]

update(_*srcObjs_, _**kwargs_)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.MutualFund.update "Link to this definition")
Update fields of the given `dataclass` object from zero or more `dataclass` source objects and/or from keyword arguments.

Return type:
[`object`](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)")

_class_ ib_async.contract.Warrant(_**kwargs_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/contract.html#Warrant)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Warrant "Link to this definition")
Warrant option.

dict()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Warrant.dict "Link to this definition")
Return dataclass values as `dict`. This is a non-recursive variant of `dataclasses.asdict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Warrant.dict "ib_async.contract.Warrant.dict")

nonDefaults()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Warrant.nonDefaults "Link to this definition")
For a `dataclass` instance get the fields that are different from the default values and return as `dict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Warrant.dict "ib_async.contract.Warrant.dict")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)"), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")]

tuple()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Warrant.tuple "Link to this definition")
Return dataclass values as `tuple`. This is a non-recursive variant of `dataclasses.astuple`.

Return type:
[`tuple`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Warrant.tuple "ib_async.contract.Warrant.tuple")[[`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)"), [`...`](https://docs.python.org/3/library/constants.html#Ellipsis "(in Python v3.14)")]

update(_*srcObjs_, _**kwargs_)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Warrant.update "Link to this definition")
Update fields of the given `dataclass` object from zero or more `dataclass` source objects and/or from keyword arguments.

Return type:
[`object`](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)")

_class_ ib_async.contract.Bag(_**kwargs_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/contract.html#Bag)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Bag "Link to this definition")
Bag contract.

dict()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Bag.dict "Link to this definition")
Return dataclass values as `dict`. This is a non-recursive variant of `dataclasses.asdict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Bag.dict "ib_async.contract.Bag.dict")

nonDefaults()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Bag.nonDefaults "Link to this definition")
For a `dataclass` instance get the fields that are different from the default values and return as `dict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Bag.dict "ib_async.contract.Bag.dict")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)"), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")]

tuple()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Bag.tuple "Link to this definition")
Return dataclass values as `tuple`. This is a non-recursive variant of `dataclasses.astuple`.

Return type:
[`tuple`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Bag.tuple "ib_async.contract.Bag.tuple")[[`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)"), [`...`](https://docs.python.org/3/library/constants.html#Ellipsis "(in Python v3.14)")]

update(_*srcObjs_, _**kwargs_)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Bag.update "Link to this definition")
Update fields of the given `dataclass` object from zero or more `dataclass` source objects and/or from keyword arguments.

Return type:
[`object`](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)")

_class_ ib_async.contract.Crypto(_symbol=''_, _exchange=''_, _currency=''_, _**kwargs_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/contract.html#Crypto)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Crypto "Link to this definition")
Crypto currency contract.

Parameters:
*   **symbol** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – Symbol name.

*   **exchange** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – Destination exchange.

*   **currency** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – Underlying currency.

dict()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Crypto.dict "Link to this definition")
Return dataclass values as `dict`. This is a non-recursive variant of `dataclasses.asdict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Crypto.dict "ib_async.contract.Crypto.dict")

nonDefaults()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Crypto.nonDefaults "Link to this definition")
For a `dataclass` instance get the fields that are different from the default values and return as `dict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Crypto.dict "ib_async.contract.Crypto.dict")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)"), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")]

tuple()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Crypto.tuple "Link to this definition")
Return dataclass values as `tuple`. This is a non-recursive variant of `dataclasses.astuple`.

Return type:
[`tuple`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Crypto.tuple "ib_async.contract.Crypto.tuple")[[`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)"), [`...`](https://docs.python.org/3/library/constants.html#Ellipsis "(in Python v3.14)")]

update(_*srcObjs_, _**kwargs_)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Crypto.update "Link to this definition")
Update fields of the given `dataclass` object from zero or more `dataclass` source objects and/or from keyword arguments.

Return type:
[`object`](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)")

_class_ ib_async.contract.TagValue(_tag_, _value_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/contract.html#TagValue)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.TagValue "Link to this definition")
Create new instance of TagValue(tag, value)

tag _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.TagValue.tag "Link to this definition")value _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.TagValue.value "Link to this definition")_class_ ib_async.contract.ComboLeg(_conId=0_, _ratio=0_, _action=''_, _exchange=''_, _openClose=0_, _shortSaleSlot=0_, _designatedLocation=''_, _exemptCode=-1_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/contract.html#ComboLeg)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ComboLeg "Link to this definition")conId _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ComboLeg.conId "Link to this definition")ratio _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ComboLeg.ratio "Link to this definition")action _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ComboLeg.action "Link to this definition")exchange _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ComboLeg.exchange "Link to this definition")openClose _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ComboLeg.openClose "Link to this definition")shortSaleSlot _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ComboLeg.shortSaleSlot "Link to this definition")designatedLocation _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ComboLeg.designatedLocation "Link to this definition")exemptCode _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=-1_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ComboLeg.exemptCode "Link to this definition")dict()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ComboLeg.dict "Link to this definition")
Return dataclass values as `dict`. This is a non-recursive variant of `dataclasses.asdict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ComboLeg.dict "ib_async.contract.ComboLeg.dict")

nonDefaults()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ComboLeg.nonDefaults "Link to this definition")
For a `dataclass` instance get the fields that are different from the default values and return as `dict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ComboLeg.dict "ib_async.contract.ComboLeg.dict")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)"), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")]

tuple()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ComboLeg.tuple "Link to this definition")
Return dataclass values as `tuple`. This is a non-recursive variant of `dataclasses.astuple`.

Return type:
[`tuple`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ComboLeg.tuple "ib_async.contract.ComboLeg.tuple")[[`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)"), [`...`](https://docs.python.org/3/library/constants.html#Ellipsis "(in Python v3.14)")]

update(_*srcObjs_, _**kwargs_)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ComboLeg.update "Link to this definition")
Update fields of the given `dataclass` object from zero or more `dataclass` source objects and/or from keyword arguments.

Return type:
[`object`](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)")

_class_ ib_async.contract.DeltaNeutralContract(_conId=0_, _delta=0.0_, _price=0.0_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/contract.html#DeltaNeutralContract)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.DeltaNeutralContract "Link to this definition")conId _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.DeltaNeutralContract.conId "Link to this definition")delta _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=0.0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.DeltaNeutralContract.delta "Link to this definition")price _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=0.0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.DeltaNeutralContract.price "Link to this definition")dict()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.DeltaNeutralContract.dict "Link to this definition")
Return dataclass values as `dict`. This is a non-recursive variant of `dataclasses.asdict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.DeltaNeutralContract.dict "ib_async.contract.DeltaNeutralContract.dict")

nonDefaults()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.DeltaNeutralContract.nonDefaults "Link to this definition")
For a `dataclass` instance get the fields that are different from the default values and return as `dict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.DeltaNeutralContract.dict "ib_async.contract.DeltaNeutralContract.dict")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)"), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")]

tuple()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.DeltaNeutralContract.tuple "Link to this definition")
Return dataclass values as `tuple`. This is a non-recursive variant of `dataclasses.astuple`.

Return type:
[`tuple`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.DeltaNeutralContract.tuple "ib_async.contract.DeltaNeutralContract.tuple")[[`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)"), [`...`](https://docs.python.org/3/library/constants.html#Ellipsis "(in Python v3.14)")]

update(_*srcObjs_, _**kwargs_)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.DeltaNeutralContract.update "Link to this definition")
Update fields of the given `dataclass` object from zero or more `dataclass` source objects and/or from keyword arguments.

Return type:
[`object`](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)")

_class_ ib_async.contract.TradingSession(_start_, _end_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/contract.html#TradingSession)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.TradingSession "Link to this definition")
Create new instance of TradingSession(start, end)

start _:[`datetime`](https://docs.python.org/3/library/datetime.html#datetime.datetime "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.TradingSession.start "Link to this definition")end _:[`datetime`](https://docs.python.org/3/library/datetime.html#datetime.datetime "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.TradingSession.end "Link to this definition")_class_ ib_async.contract.ContractDetails(_contract=None_, _marketName=''_, _minTick=0.0_, _orderTypes=''_, _validExchanges=''_, _priceMagnifier=0_, _underConId=0_, _longName=''_, _contractMonth=''_, _industry=''_, _category=''_, _subcategory=''_, _timeZoneId=''_, _tradingHours=''_, _liquidHours=''_, _evRule=''_, _evMultiplier=0_, _mdSizeMultiplier=1_, _aggGroup=0_, _underSymbol=''_, _underSecType=''_, _marketRuleIds=''_, _secIdList=<factory>_, _realExpirationDate=''_, _lastTradeTime=''_, _stockType=''_, _minSize=0.0_, _sizeIncrement=0.0_, _suggestedSizeIncrement=0.0_, _cusip=''_, _ratings=''_, _descAppend=''_, _bondType=''_, _couponType=''_, _callable=False_, _putable=False_, _coupon=0_, _convertible=False_, _maturity=''_, _issueDate=''_, _nextOptionDate=''_, _nextOptionType=''_, _nextOptionPartial=False_, _notes=''_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/contract.html#ContractDetails)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ContractDetails "Link to this definition")contract _:[`Contract`](https://ib-api-reloaded.github.io/ib\_async/api.html#ib\_async.contract.Contract "ib\_async.contract.Contract")|[`None`](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")_ _=None_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ContractDetails.contract "Link to this definition")marketName _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ContractDetails.marketName "Link to this definition")minTick _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=0.0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ContractDetails.minTick "Link to this definition")orderTypes _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ContractDetails.orderTypes "Link to this definition")validExchanges _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ContractDetails.validExchanges "Link to this definition")priceMagnifier _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ContractDetails.priceMagnifier "Link to this definition")underConId _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ContractDetails.underConId "Link to this definition")longName _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ContractDetails.longName "Link to this definition")contractMonth _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ContractDetails.contractMonth "Link to this definition")industry _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ContractDetails.industry "Link to this definition")category _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ContractDetails.category "Link to this definition")subcategory _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ContractDetails.subcategory "Link to this definition")timeZoneId _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ContractDetails.timeZoneId "Link to this definition")tradingHours _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ContractDetails.tradingHours "Link to this definition")liquidHours _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ContractDetails.liquidHours "Link to this definition")evRule _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ContractDetails.evRule "Link to this definition")evMultiplier _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ContractDetails.evMultiplier "Link to this definition")mdSizeMultiplier _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=1_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ContractDetails.mdSizeMultiplier "Link to this definition")aggGroup _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ContractDetails.aggGroup "Link to this definition")underSymbol _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ContractDetails.underSymbol "Link to this definition")underSecType _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ContractDetails.underSecType "Link to this definition")marketRuleIds _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ContractDetails.marketRuleIds "Link to this definition")secIdList _:[`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`TagValue`](https://ib-api-reloaded.github.io/ib\_async/api.html#ib\_async.contract.TagValue "ib\_async.contract.TagValue")]_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ContractDetails.secIdList "Link to this definition")realExpirationDate _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ContractDetails.realExpirationDate "Link to this definition")lastTradeTime _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ContractDetails.lastTradeTime "Link to this definition")stockType _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ContractDetails.stockType "Link to this definition")minSize _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=0.0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ContractDetails.minSize "Link to this definition")sizeIncrement _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=0.0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ContractDetails.sizeIncrement "Link to this definition")suggestedSizeIncrement _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=0.0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ContractDetails.suggestedSizeIncrement "Link to this definition")cusip _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ContractDetails.cusip "Link to this definition")ratings _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ContractDetails.ratings "Link to this definition")descAppend _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ContractDetails.descAppend "Link to this definition")bondType _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ContractDetails.bondType "Link to this definition")couponType _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ContractDetails.couponType "Link to this definition")callable _:[`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")_ _=False_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ContractDetails.callable "Link to this definition")putable _:[`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")_ _=False_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ContractDetails.putable "Link to this definition")coupon _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ContractDetails.coupon "Link to this definition")convertible _:[`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")_ _=False_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ContractDetails.convertible "Link to this definition")maturity _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ContractDetails.maturity "Link to this definition")issueDate _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ContractDetails.issueDate "Link to this definition")nextOptionDate _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ContractDetails.nextOptionDate "Link to this definition")nextOptionType _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ContractDetails.nextOptionType "Link to this definition")nextOptionPartial _:[`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")_ _=False_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ContractDetails.nextOptionPartial "Link to this definition")notes _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ContractDetails.notes "Link to this definition")tradingSessions()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/contract.html#ContractDetails.tradingSessions)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ContractDetails.tradingSessions "Link to this definition")Return type:
[`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`TradingSession`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.TradingSession "ib_async.contract.TradingSession")]

liquidSessions()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/contract.html#ContractDetails.liquidSessions)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ContractDetails.liquidSessions "Link to this definition")Return type:
[`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`TradingSession`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.TradingSession "ib_async.contract.TradingSession")]

dict()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ContractDetails.dict "Link to this definition")
Return dataclass values as `dict`. This is a non-recursive variant of `dataclasses.asdict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ContractDetails.dict "ib_async.contract.ContractDetails.dict")

nonDefaults()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ContractDetails.nonDefaults "Link to this definition")
For a `dataclass` instance get the fields that are different from the default values and return as `dict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ContractDetails.dict "ib_async.contract.ContractDetails.dict")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)"), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")]

tuple()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ContractDetails.tuple "Link to this definition")
Return dataclass values as `tuple`. This is a non-recursive variant of `dataclasses.astuple`.

Return type:
[`tuple`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ContractDetails.tuple "ib_async.contract.ContractDetails.tuple")[[`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)"), [`...`](https://docs.python.org/3/library/constants.html#Ellipsis "(in Python v3.14)")]

update(_*srcObjs_, _**kwargs_)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ContractDetails.update "Link to this definition")
Update fields of the given `dataclass` object from zero or more `dataclass` source objects and/or from keyword arguments.

Return type:
[`object`](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)")

_class_ ib_async.contract.ContractDescription(_contract=None_, _derivativeSecTypes=<factory>_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/contract.html#ContractDescription)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ContractDescription "Link to this definition")contract _:[`Contract`](https://ib-api-reloaded.github.io/ib\_async/api.html#ib\_async.contract.Contract "ib\_async.contract.Contract")|[`None`](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")_ _=None_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ContractDescription.contract "Link to this definition")derivativeSecTypes _:[`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")]_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ContractDescription.derivativeSecTypes "Link to this definition")dict()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ContractDescription.dict "Link to this definition")
Return dataclass values as `dict`. This is a non-recursive variant of `dataclasses.asdict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ContractDescription.dict "ib_async.contract.ContractDescription.dict")

nonDefaults()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ContractDescription.nonDefaults "Link to this definition")
For a `dataclass` instance get the fields that are different from the default values and return as `dict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ContractDescription.dict "ib_async.contract.ContractDescription.dict")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)"), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")]

tuple()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ContractDescription.tuple "Link to this definition")
Return dataclass values as `tuple`. This is a non-recursive variant of `dataclasses.astuple`.

Return type:
[`tuple`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ContractDescription.tuple "ib_async.contract.ContractDescription.tuple")[[`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)"), [`...`](https://docs.python.org/3/library/constants.html#Ellipsis "(in Python v3.14)")]

update(_*srcObjs_, _**kwargs_)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ContractDescription.update "Link to this definition")
Update fields of the given `dataclass` object from zero or more `dataclass` source objects and/or from keyword arguments.

Return type:
[`object`](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)")

_class_ ib_async.contract.ScanData(_rank_, _contractDetails_, _distance_, _benchmark_, _projection_, _legsStr_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/contract.html#ScanData)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ScanData "Link to this definition")rank _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ScanData.rank "Link to this definition")contractDetails _:[`ContractDetails`](https://ib-api-reloaded.github.io/ib\_async/api.html#ib\_async.contract.ContractDetails "ib\_async.contract.ContractDetails")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ScanData.contractDetails "Link to this definition")distance _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ScanData.distance "Link to this definition")benchmark _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ScanData.benchmark "Link to this definition")projection _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ScanData.projection "Link to this definition")legsStr _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ScanData.legsStr "Link to this definition")dict()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ScanData.dict "Link to this definition")
Return dataclass values as `dict`. This is a non-recursive variant of `dataclasses.asdict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ScanData.dict "ib_async.contract.ScanData.dict")

nonDefaults()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ScanData.nonDefaults "Link to this definition")
For a `dataclass` instance get the fields that are different from the default values and return as `dict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ScanData.dict "ib_async.contract.ScanData.dict")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)"), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")]

tuple()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ScanData.tuple "Link to this definition")
Return dataclass values as `tuple`. This is a non-recursive variant of `dataclasses.astuple`.

Return type:
[`tuple`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ScanData.tuple "ib_async.contract.ScanData.tuple")[[`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)"), [`...`](https://docs.python.org/3/library/constants.html#Ellipsis "(in Python v3.14)")]

update(_*srcObjs_, _**kwargs_)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ScanData.update "Link to this definition")
Update fields of the given `dataclass` object from zero or more `dataclass` source objects and/or from keyword arguments.

Return type:
[`object`](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)")

Ticker[](https://ib-api-reloaded.github.io/ib_async/api.html#module-ib_async.ticker "Link to this heading")
------------------------------------------------------------------------------------------------------------

Access to realtime market information.

_class_ ib_async.ticker.Ticker(_contract=None_, _time=None_, _timestamp=None_, _marketDataType=1_, _minTick=nan_, _bid=nan_, _bidSize=nan_, _bidExchange=''_, _ask=nan_, _askSize=nan_, _askExchange=''_, _last=nan_, _lastSize=nan_, _lastExchange=''_, _lastTimestamp=None_, _prevBid=nan_, _prevBidSize=nan_, _prevAsk=nan_, _prevAskSize=nan_, _prevLast=nan_, _prevLastSize=nan_, _volume=nan_, _open=nan_, _high=nan_, _low=nan_, _close=nan_, _vwap=nan_, _low13week=nan_, _high13week=nan_, _low26week=nan_, _high26week=nan_, _low52week=nan_, _high52week=nan_, _bidYield=nan_, _askYield=nan_, _lastYield=nan_, _markPrice=nan_, _halted=nan_, _rtHistVolatility=nan_, _rtVolume=nan_, _rtTradeVolume=nan_, _rtTime=None_, _avVolume=nan_, _tradeCount=nan_, _tradeRate=nan_, _volumeRate=nan_, _volumeRate3Min=nan_, _volumeRate5Min=nan_, _volumeRate10Min=nan_, _shortable=nan_, _shortableShares=nan_, _indexFuturePremium=nan_, _futuresOpenInterest=nan_, _putOpenInterest=nan_, _callOpenInterest=nan_, _putVolume=nan_, _callVolume=nan_, _avOptionVolume=nan_, _histVolatility=nan_, _impliedVolatility=nan_, _openInterest=nan_, _lastRthTrade=nan_, _lastRegTime=''_, _optionBidExch=''_, _optionAskExch=''_, _bondFactorMultiplier=nan_, _creditmanMarkPrice=nan_, _creditmanSlowMarkPrice=nan_, _delayedLastTimestamp=None_, _delayedHalted=nan_, _reutersMutualFunds=''_, _etfNavClose=nan_, _etfNavPriorClose=nan_, _etfNavBid=nan_, _etfNavAsk=nan_, _etfNavLast=nan_, _etfFrozenNavLast=nan_, _etfNavHigh=nan_, _etfNavLow=nan_, _socialMarketAnalytics=''_, _estimatedIpoMidpoint=nan_, _finalIpoLast=nan_, _dividends=None_, _fundamentalRatios=None_, _ticks=<factory>_, _tickByTicks=<factory>_, _domBids=<factory>_, _domBidsDict=<factory>_, _domAsks=<factory>_, _domAsksDict=<factory>_, _domTicks=<factory>_, _bidGreeks=None_, _askGreeks=None_, _lastGreeks=None_, _modelGreeks=None_, _custGreeks=None_, _bidEfp=None_, _askEfp=None_, _lastEfp=None_, _openEfp=None_, _highEfp=None_, _lowEfp=None_, _closeEfp=None_, _auctionVolume=nan_, _auctionPrice=nan_, _auctionImbalance=nan_, _regulatoryImbalance=nan_, _bboExchange=''_, _snapshotPermissions=0_, _defaults=<factory>_, _created=False_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ticker.html#Ticker)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker "Link to this definition")
Current market data such as bid, ask, last price, etc. for a contract.

Streaming level-1 ticks of type [`TickData`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.TickData "ib_async.objects.TickData") are stored in the `ticks` list.

Streaming level-2 ticks of type [`MktDepthData`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.MktDepthData "ib_async.objects.MktDepthData") are stored in the `domTicks` list. The order book (DOM) is available as lists of [`DOMLevel`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.DOMLevel "ib_async.objects.DOMLevel") in `domBids` and `domAsks`.

Streaming tick-by-tick ticks are stored in `tickByTicks`.

For options the [`OptionComputation`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.OptionComputation "ib_async.objects.OptionComputation") values for the bid, ask, resp. last price are stored in the `bidGreeks`, `askGreeks` resp. `lastGreeks` attributes. There is also `modelGreeks` that conveys the greeks as calculated by Interactive Brokers’ option model.

Events:
*   `updateEvent` (ticker: [`Ticker`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker "ib_async.ticker.Ticker"))

events _:[`ClassVar`](https://docs.python.org/3/library/typing.html#typing.ClassVar "(in Python v3.14)")_ _=('updateEvent',)_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.events "Link to this definition")contract _:[`Contract`](https://ib-api-reloaded.github.io/ib\_async/api.html#ib\_async.contract.Contract "ib\_async.contract.Contract")|[`None`](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")_ _=None_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.contract "Link to this definition")time _:[`datetime`](https://docs.python.org/3/library/datetime.html#datetime.datetime "(in Python v3.14)")|[`None`](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")_ _=None_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.time "Link to this definition")timestamp _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")|[`None`](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")_ _=None_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.timestamp "Link to this definition")marketDataType _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=1_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.marketDataType "Link to this definition")minTick _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.minTick "Link to this definition")bid _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.bid "Link to this definition")bidSize _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.bidSize "Link to this definition")bidExchange _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.bidExchange "Link to this definition")ask _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.ask "Link to this definition")askSize _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.askSize "Link to this definition")askExchange _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.askExchange "Link to this definition")last _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.last "Link to this definition")lastSize _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.lastSize "Link to this definition")lastExchange _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.lastExchange "Link to this definition")lastTimestamp _:[`datetime`](https://docs.python.org/3/library/datetime.html#datetime.datetime "(in Python v3.14)")|[`None`](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")_ _=None_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.lastTimestamp "Link to this definition")prevBid _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.prevBid "Link to this definition")prevBidSize _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.prevBidSize "Link to this definition")prevAsk _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.prevAsk "Link to this definition")prevAskSize _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.prevAskSize "Link to this definition")prevLast _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.prevLast "Link to this definition")prevLastSize _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.prevLastSize "Link to this definition")volume _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.volume "Link to this definition")open _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.open "Link to this definition")high _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.high "Link to this definition")low _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.low "Link to this definition")close _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.close "Link to this definition")vwap _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.vwap "Link to this definition")low13week _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.low13week "Link to this definition")high13week _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.high13week "Link to this definition")low26week _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.low26week "Link to this definition")high26week _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.high26week "Link to this definition")low52week _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.low52week "Link to this definition")high52week _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.high52week "Link to this definition")bidYield _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.bidYield "Link to this definition")askYield _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.askYield "Link to this definition")lastYield _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.lastYield "Link to this definition")markPrice _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.markPrice "Link to this definition")halted _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.halted "Link to this definition")rtHistVolatility _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.rtHistVolatility "Link to this definition")rtVolume _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.rtVolume "Link to this definition")rtTradeVolume _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.rtTradeVolume "Link to this definition")rtTime _:[`datetime`](https://docs.python.org/3/library/datetime.html#datetime.datetime "(in Python v3.14)")|[`None`](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")_ _=None_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.rtTime "Link to this definition")avVolume _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.avVolume "Link to this definition")tradeCount _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.tradeCount "Link to this definition")tradeRate _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.tradeRate "Link to this definition")volumeRate _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.volumeRate "Link to this definition")volumeRate3Min _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.volumeRate3Min "Link to this definition")volumeRate5Min _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.volumeRate5Min "Link to this definition")volumeRate10Min _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.volumeRate10Min "Link to this definition")shortable _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.shortable "Link to this definition")shortableShares _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.shortableShares "Link to this definition")indexFuturePremium _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.indexFuturePremium "Link to this definition")futuresOpenInterest _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.futuresOpenInterest "Link to this definition")putOpenInterest _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.putOpenInterest "Link to this definition")callOpenInterest _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.callOpenInterest "Link to this definition")putVolume _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.putVolume "Link to this definition")callVolume _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.callVolume "Link to this definition")avOptionVolume _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.avOptionVolume "Link to this definition")histVolatility _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.histVolatility "Link to this definition")impliedVolatility _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.impliedVolatility "Link to this definition")openInterest _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.openInterest "Link to this definition")lastRthTrade _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.lastRthTrade "Link to this definition")lastRegTime _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.lastRegTime "Link to this definition")optionBidExch _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.optionBidExch "Link to this definition")optionAskExch _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.optionAskExch "Link to this definition")bondFactorMultiplier _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.bondFactorMultiplier "Link to this definition")creditmanMarkPrice _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.creditmanMarkPrice "Link to this definition")creditmanSlowMarkPrice _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.creditmanSlowMarkPrice "Link to this definition")delayedLastTimestamp _:[`datetime`](https://docs.python.org/3/library/datetime.html#datetime.datetime "(in Python v3.14)")|[`None`](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")_ _=None_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.delayedLastTimestamp "Link to this definition")delayedHalted _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.delayedHalted "Link to this definition")reutersMutualFunds _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.reutersMutualFunds "Link to this definition")etfNavClose _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.etfNavClose "Link to this definition")etfNavPriorClose _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.etfNavPriorClose "Link to this definition")etfNavBid _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.etfNavBid "Link to this definition")etfNavAsk _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.etfNavAsk "Link to this definition")etfNavLast _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.etfNavLast "Link to this definition")etfFrozenNavLast _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.etfFrozenNavLast "Link to this definition")etfNavHigh _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.etfNavHigh "Link to this definition")etfNavLow _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.etfNavLow "Link to this definition")socialMarketAnalytics _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.socialMarketAnalytics "Link to this definition")estimatedIpoMidpoint _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.estimatedIpoMidpoint "Link to this definition")finalIpoLast _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.finalIpoLast "Link to this definition")dividends _:[`Dividends`](https://ib-api-reloaded.github.io/ib\_async/api.html#ib\_async.objects.Dividends "ib\_async.objects.Dividends")|[`None`](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")_ _=None_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.dividends "Link to this definition")fundamentalRatios _:[`FundamentalRatios`](https://ib-api-reloaded.github.io/ib\_async/api.html#ib\_async.objects.FundamentalRatios "ib\_async.objects.FundamentalRatios")|[`None`](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")_ _=None_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.fundamentalRatios "Link to this definition")ticks _:[`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`TickData`](https://ib-api-reloaded.github.io/ib\_async/api.html#ib\_async.objects.TickData "ib\_async.objects.TickData")]_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.ticks "Link to this definition")tickByTicks _:[`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`TickByTickAllLast`](https://ib-api-reloaded.github.io/ib\_async/api.html#ib\_async.objects.TickByTickAllLast "ib\_async.objects.TickByTickAllLast")|[`TickByTickBidAsk`](https://ib-api-reloaded.github.io/ib\_async/api.html#ib\_async.objects.TickByTickBidAsk "ib\_async.objects.TickByTickBidAsk")|[`TickByTickMidPoint`](https://ib-api-reloaded.github.io/ib\_async/api.html#ib\_async.objects.TickByTickMidPoint "ib\_async.objects.TickByTickMidPoint")]_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.tickByTicks "Link to this definition")domBids _:[`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`DOMLevel`](https://ib-api-reloaded.github.io/ib\_async/api.html#ib\_async.objects.DOMLevel "ib\_async.objects.DOMLevel")]_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.domBids "Link to this definition")domBidsDict _:[`dict`](https://ib-api-reloaded.github.io/ib\_async/api.html#ib\_async.ticker.Ticker.dict "ib\_async.ticker.Ticker.dict")[[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)"),[`DOMLevel`](https://ib-api-reloaded.github.io/ib\_async/api.html#ib\_async.objects.DOMLevel "ib\_async.objects.DOMLevel")]_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.domBidsDict "Link to this definition")domAsks _:[`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`DOMLevel`](https://ib-api-reloaded.github.io/ib\_async/api.html#ib\_async.objects.DOMLevel "ib\_async.objects.DOMLevel")]_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.domAsks "Link to this definition")domAsksDict _:[`dict`](https://ib-api-reloaded.github.io/ib\_async/api.html#ib\_async.ticker.Ticker.dict "ib\_async.ticker.Ticker.dict")[[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)"),[`DOMLevel`](https://ib-api-reloaded.github.io/ib\_async/api.html#ib\_async.objects.DOMLevel "ib\_async.objects.DOMLevel")]_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.domAsksDict "Link to this definition")domTicks _:[`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`MktDepthData`](https://ib-api-reloaded.github.io/ib\_async/api.html#ib\_async.objects.MktDepthData "ib\_async.objects.MktDepthData")]_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.domTicks "Link to this definition")bidGreeks _:[`OptionComputation`](https://ib-api-reloaded.github.io/ib\_async/api.html#ib\_async.objects.OptionComputation "ib\_async.objects.OptionComputation")|[`None`](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")_ _=None_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.bidGreeks "Link to this definition")askGreeks _:[`OptionComputation`](https://ib-api-reloaded.github.io/ib\_async/api.html#ib\_async.objects.OptionComputation "ib\_async.objects.OptionComputation")|[`None`](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")_ _=None_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.askGreeks "Link to this definition")lastGreeks _:[`OptionComputation`](https://ib-api-reloaded.github.io/ib\_async/api.html#ib\_async.objects.OptionComputation "ib\_async.objects.OptionComputation")|[`None`](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")_ _=None_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.lastGreeks "Link to this definition")modelGreeks _:[`OptionComputation`](https://ib-api-reloaded.github.io/ib\_async/api.html#ib\_async.objects.OptionComputation "ib\_async.objects.OptionComputation")|[`None`](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")_ _=None_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.modelGreeks "Link to this definition")custGreeks _:[`OptionComputation`](https://ib-api-reloaded.github.io/ib\_async/api.html#ib\_async.objects.OptionComputation "ib\_async.objects.OptionComputation")|[`None`](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")_ _=None_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.custGreeks "Link to this definition")bidEfp _:[`EfpData`](https://ib-api-reloaded.github.io/ib\_async/api.html#ib\_async.objects.EfpData "ib\_async.objects.EfpData")|[`None`](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")_ _=None_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.bidEfp "Link to this definition")askEfp _:[`EfpData`](https://ib-api-reloaded.github.io/ib\_async/api.html#ib\_async.objects.EfpData "ib\_async.objects.EfpData")|[`None`](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")_ _=None_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.askEfp "Link to this definition")lastEfp _:[`EfpData`](https://ib-api-reloaded.github.io/ib\_async/api.html#ib\_async.objects.EfpData "ib\_async.objects.EfpData")|[`None`](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")_ _=None_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.lastEfp "Link to this definition")openEfp _:[`EfpData`](https://ib-api-reloaded.github.io/ib\_async/api.html#ib\_async.objects.EfpData "ib\_async.objects.EfpData")|[`None`](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")_ _=None_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.openEfp "Link to this definition")highEfp _:[`EfpData`](https://ib-api-reloaded.github.io/ib\_async/api.html#ib\_async.objects.EfpData "ib\_async.objects.EfpData")|[`None`](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")_ _=None_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.highEfp "Link to this definition")lowEfp _:[`EfpData`](https://ib-api-reloaded.github.io/ib\_async/api.html#ib\_async.objects.EfpData "ib\_async.objects.EfpData")|[`None`](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")_ _=None_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.lowEfp "Link to this definition")closeEfp _:[`EfpData`](https://ib-api-reloaded.github.io/ib\_async/api.html#ib\_async.objects.EfpData "ib\_async.objects.EfpData")|[`None`](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")_ _=None_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.closeEfp "Link to this definition")auctionVolume _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.auctionVolume "Link to this definition")auctionPrice _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.auctionPrice "Link to this definition")auctionImbalance _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.auctionImbalance "Link to this definition")regulatoryImbalance _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.regulatoryImbalance "Link to this definition")bboExchange _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.bboExchange "Link to this definition")snapshotPermissions _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.snapshotPermissions "Link to this definition")defaults _:[`IBDefaults`](https://ib-api-reloaded.github.io/ib\_async/api.html#ib\_async.objects.IBDefaults "ib\_async.objects.IBDefaults")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.defaults "Link to this definition")created _:[`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")_ _=False_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.created "Link to this definition")isUnset(_value_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ticker.html#Ticker.isUnset)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.isUnset "Link to this definition")Return type:
[`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")

hasBidAsk()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ticker.html#Ticker.hasBidAsk)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.hasBidAsk "Link to this definition")
See if this ticker has a valid bid and ask.

Return type:
[`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")

midpoint()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ticker.html#Ticker.midpoint)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.midpoint "Link to this definition")
Return average of bid and ask, or defaults.unset if no valid bid and ask are available.

Return type:
[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")

marketPrice()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ticker.html#Ticker.marketPrice)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.marketPrice "Link to this definition")
Return the first available one of :rtype: [`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")

*   last price if within current bid/ask or no bid/ask available;

*   average of bid and ask (midpoint).

dict()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.dict "Link to this definition")
Return dataclass values as `dict`. This is a non-recursive variant of `dataclasses.asdict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.dict "ib_async.ticker.Ticker.dict")

nonDefaults()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.nonDefaults "Link to this definition")
For a `dataclass` instance get the fields that are different from the default values and return as `dict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.dict "ib_async.ticker.Ticker.dict")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)"), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")]

tuple()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.tuple "Link to this definition")
Return dataclass values as `tuple`. This is a non-recursive variant of `dataclasses.astuple`.

Return type:
[`tuple`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.tuple "ib_async.ticker.Ticker.tuple")[[`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)"), [`...`](https://docs.python.org/3/library/constants.html#Ellipsis "(in Python v3.14)")]

update(_*srcObjs_, _**kwargs_)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Ticker.update "Link to this definition")
Update fields of the given `dataclass` object from zero or more `dataclass` source objects and/or from keyword arguments.

Return type:
[`object`](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)")

_class_ ib_async.ticker.TickerUpdateEvent(_\_name=''_, _\_with\_error\_done\_events=True_, _error\_event=None_, _done\_event=None_, _\_value=<NoValue>_, _\_slots=<factory>_, _\_done=False_, _\_source=None_, _\_\_weakref\_\_=None_, _\_task=None_, _NO\_VALUE=<NoValue>_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ticker.html#TickerUpdateEvent)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.TickerUpdateEvent "Link to this definition")trades()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ticker.html#TickerUpdateEvent.trades)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.TickerUpdateEvent.trades "Link to this definition")
Emit trade ticks.

Return type:
[`Tickfilter`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Tickfilter "ib_async.ticker.Tickfilter")

bids()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ticker.html#TickerUpdateEvent.bids)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.TickerUpdateEvent.bids "Link to this definition")
Emit bid ticks.

Return type:
[`Tickfilter`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Tickfilter "ib_async.ticker.Tickfilter")

asks()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ticker.html#TickerUpdateEvent.asks)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.TickerUpdateEvent.asks "Link to this definition")
Emit ask ticks.

Return type:
[`Tickfilter`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Tickfilter "ib_async.ticker.Tickfilter")

bidasks()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ticker.html#TickerUpdateEvent.bidasks)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.TickerUpdateEvent.bidasks "Link to this definition")
Emit bid and ask ticks.

Return type:
[`Tickfilter`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Tickfilter "ib_async.ticker.Tickfilter")

midpoints()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ticker.html#TickerUpdateEvent.midpoints)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.TickerUpdateEvent.midpoints "Link to this definition")
Emit midpoint ticks.

Return type:
[`Tickfilter`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Tickfilter "ib_async.ticker.Tickfilter")

_class_ ib_async.ticker.Tickfilter(_tickTypes_, _source=None_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ticker.html#Tickfilter)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Tickfilter "Link to this definition")
Tick filtering event operators that `emit(time, price, size)`.

on_source(_ticker_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ticker.html#Tickfilter.on_source)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Tickfilter.on_source "Link to this definition")
Emit a new value to all connected listeners.

Parameters:
**args** – Argument values to emit to listeners.

timebars(_timer_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ticker.html#Tickfilter.timebars)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Tickfilter.timebars "Link to this definition")
Aggregate ticks into time bars, where the timing of new bars is derived from a timer event. Emits a completed [`Bar`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Bar "ib_async.ticker.Bar").

This event stores a [`BarList`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.BarList "ib_async.ticker.BarList") of all created bars in the `bars` property.

Parameters:
**timer** ([`Event`](https://eventkit.readthedocs.io/en/latest/api.html#eventkit.event.Event "(in eventkit v1.0)")) – Event for timing when a new bar starts.

Return type:
[`TimeBars`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.TimeBars "ib_async.ticker.TimeBars")

tickbars(_count_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ticker.html#Tickfilter.tickbars)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Tickfilter.tickbars "Link to this definition")
Aggregate ticks into bars that have the same number of ticks. Emits a completed [`Bar`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Bar "ib_async.ticker.Bar").

This event stores a [`BarList`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.BarList "ib_async.ticker.BarList") of all created bars in the `bars` property.

Parameters:
**count** ([`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) – Number of ticks to use to form one bar.

Return type:
[`TickBars`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.TickBars "ib_async.ticker.TickBars")

volumebars(_volume_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ticker.html#Tickfilter.volumebars)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Tickfilter.volumebars "Link to this definition")
Aggregate ticks into bars that have the same volume. Emits a completed [`Bar`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Bar "ib_async.ticker.Bar").

This event stores a [`BarList`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.BarList "ib_async.ticker.BarList") of all created bars in the `bars` property.

Parameters:
**count** – Number of ticks to use to form one bar.

Return type:
[`VolumeBars`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.VolumeBars "ib_async.ticker.VolumeBars")

_class_ ib_async.ticker.Midpoints(_tickTypes_, _source=None_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ticker.html#Midpoints)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Midpoints "Link to this definition")on_source(_ticker_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ticker.html#Midpoints.on_source)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Midpoints.on_source "Link to this definition")
Emit a new value to all connected listeners.

Parameters:
**args** – Argument values to emit to listeners.

_class_ ib_async.ticker.Bar(_time_, _open=nan_, _high=nan_, _low=nan_, _close=nan_, _volume=0_, _count=0_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ticker.html#Bar)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Bar "Link to this definition")time _:[`datetime`](https://docs.python.org/3/library/datetime.html#datetime.datetime "(in Python v3.14)")|[`None`](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Bar.time "Link to this definition")open _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Bar.open "Link to this definition")high _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Bar.high "Link to this definition")low _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Bar.low "Link to this definition")close _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Bar.close "Link to this definition")volume _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Bar.volume "Link to this definition")count _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Bar.count "Link to this definition")_class_ ib_async.ticker.BarList(_*args_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ticker.html#BarList)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.BarList "Link to this definition")_class_ ib_async.ticker.TimeBars(_timer_, _source=None_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ticker.html#TimeBars)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.TimeBars "Link to this definition")
Aggregate ticks into time bars, where the timing of new bars is derived from a timer event. Emits a completed [`Bar`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Bar "ib_async.ticker.Bar").

This event stores a [`BarList`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.BarList "ib_async.ticker.BarList") of all created bars in the `bars` property.

Parameters:
**timer** – Event for timing when a new bar starts.

bars _:[`BarList`](https://ib-api-reloaded.github.io/ib\_async/api.html#ib\_async.ticker.BarList "ib\_async.ticker.BarList")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.TimeBars.bars "Link to this definition")on_source(_time_, _price_, _size_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ticker.html#TimeBars.on_source)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.TimeBars.on_source "Link to this definition")
Emit a new value to all connected listeners.

Parameters:
**args** – Argument values to emit to listeners.

_class_ ib_async.ticker.TickBars(_count_, _source=None_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ticker.html#TickBars)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.TickBars "Link to this definition")
Aggregate ticks into bars that have the same number of ticks. Emits a completed [`Bar`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Bar "ib_async.ticker.Bar").

This event stores a [`BarList`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.BarList "ib_async.ticker.BarList") of all created bars in the `bars` property.

Parameters:
**count** – Number of ticks to use to form one bar.

bars _:[`BarList`](https://ib-api-reloaded.github.io/ib\_async/api.html#ib\_async.ticker.BarList "ib\_async.ticker.BarList")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.TickBars.bars "Link to this definition")on_source(_time_, _price_, _size_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ticker.html#TickBars.on_source)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.TickBars.on_source "Link to this definition")
Emit a new value to all connected listeners.

Parameters:
**args** – Argument values to emit to listeners.

_class_ ib_async.ticker.VolumeBars(_volume_, _source=None_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ticker.html#VolumeBars)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.VolumeBars "Link to this definition")
Aggregate ticks into bars that have the same volume. Emits a completed [`Bar`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.Bar "ib_async.ticker.Bar").

This event stores a [`BarList`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.BarList "ib_async.ticker.BarList") of all created bars in the `bars` property.

Parameters:
**count** – Number of ticks to use to form one bar.

bars _:[`BarList`](https://ib-api-reloaded.github.io/ib\_async/api.html#ib\_async.ticker.BarList "ib\_async.ticker.BarList")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.VolumeBars.bars "Link to this definition")on_source(_time_, _price_, _size_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ticker.html#VolumeBars.on_source)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ticker.VolumeBars.on_source "Link to this definition")
Emit a new value to all connected listeners.

Parameters:
**args** – Argument values to emit to listeners.

Objects[](https://ib-api-reloaded.github.io/ib_async/api.html#module-ib_async.objects "Link to this heading")
--------------------------------------------------------------------------------------------------------------

Object hierarchy.

_class_ ib_async.objects.ScannerSubscription(_numberOfRows=-1_, _instrument=''_, _locationCode=''_, _scanCode=''_, _abovePrice=1.7976931348623157e+308_, _belowPrice=1.7976931348623157e+308_, _aboveVolume=2147483647_, _marketCapAbove=1.7976931348623157e+308_, _marketCapBelow=1.7976931348623157e+308_, _moodyRatingAbove=''_, _moodyRatingBelow=''_, _spRatingAbove=''_, _spRatingBelow=''_, _maturityDateAbove=''_, _maturityDateBelow=''_, _couponRateAbove=1.7976931348623157e+308_, _couponRateBelow=1.7976931348623157e+308_, _excludeConvertible=False_, _averageOptionVolumeAbove=2147483647_, _scannerSettingPairs=''_, _stockTypeFilter=''_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/objects.html#ScannerSubscription)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.ScannerSubscription "Link to this definition")numberOfRows _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=-1_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.ScannerSubscription.numberOfRows "Link to this definition")instrument _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.ScannerSubscription.instrument "Link to this definition")locationCode _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.ScannerSubscription.locationCode "Link to this definition")scanCode _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.ScannerSubscription.scanCode "Link to this definition")abovePrice _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=1.7976931348623157e+308_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.ScannerSubscription.abovePrice "Link to this definition")belowPrice _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=1.7976931348623157e+308_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.ScannerSubscription.belowPrice "Link to this definition")aboveVolume _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=2147483647_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.ScannerSubscription.aboveVolume "Link to this definition")marketCapAbove _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=1.7976931348623157e+308_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.ScannerSubscription.marketCapAbove "Link to this definition")marketCapBelow _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=1.7976931348623157e+308_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.ScannerSubscription.marketCapBelow "Link to this definition")moodyRatingAbove _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.ScannerSubscription.moodyRatingAbove "Link to this definition")moodyRatingBelow _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.ScannerSubscription.moodyRatingBelow "Link to this definition")spRatingAbove _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.ScannerSubscription.spRatingAbove "Link to this definition")spRatingBelow _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.ScannerSubscription.spRatingBelow "Link to this definition")maturityDateAbove _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.ScannerSubscription.maturityDateAbove "Link to this definition")maturityDateBelow _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.ScannerSubscription.maturityDateBelow "Link to this definition")couponRateAbove _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=1.7976931348623157e+308_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.ScannerSubscription.couponRateAbove "Link to this definition")couponRateBelow _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=1.7976931348623157e+308_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.ScannerSubscription.couponRateBelow "Link to this definition")excludeConvertible _:[`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")_ _=False_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.ScannerSubscription.excludeConvertible "Link to this definition")averageOptionVolumeAbove _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=2147483647_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.ScannerSubscription.averageOptionVolumeAbove "Link to this definition")scannerSettingPairs _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.ScannerSubscription.scannerSettingPairs "Link to this definition")stockTypeFilter _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.ScannerSubscription.stockTypeFilter "Link to this definition")dict()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.ScannerSubscription.dict "Link to this definition")
Return dataclass values as `dict`. This is a non-recursive variant of `dataclasses.asdict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.ScannerSubscription.dict "ib_async.objects.ScannerSubscription.dict")

nonDefaults()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.ScannerSubscription.nonDefaults "Link to this definition")
For a `dataclass` instance get the fields that are different from the default values and return as `dict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.ScannerSubscription.dict "ib_async.objects.ScannerSubscription.dict")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)"), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")]

tuple()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.ScannerSubscription.tuple "Link to this definition")
Return dataclass values as `tuple`. This is a non-recursive variant of `dataclasses.astuple`.

Return type:
[`tuple`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.ScannerSubscription.tuple "ib_async.objects.ScannerSubscription.tuple")[[`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)"), [`...`](https://docs.python.org/3/library/constants.html#Ellipsis "(in Python v3.14)")]

update(_*srcObjs_, _**kwargs_)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.ScannerSubscription.update "Link to this definition")
Update fields of the given `dataclass` object from zero or more `dataclass` source objects and/or from keyword arguments.

Return type:
[`object`](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)")

_class_ ib_async.objects.SoftDollarTier(_name=''_, _val=''_, _displayName=''_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/objects.html#SoftDollarTier)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.SoftDollarTier "Link to this definition")name _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.SoftDollarTier.name "Link to this definition")val _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.SoftDollarTier.val "Link to this definition")displayName _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.SoftDollarTier.displayName "Link to this definition")dict()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.SoftDollarTier.dict "Link to this definition")
Return dataclass values as `dict`. This is a non-recursive variant of `dataclasses.asdict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.SoftDollarTier.dict "ib_async.objects.SoftDollarTier.dict")

nonDefaults()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.SoftDollarTier.nonDefaults "Link to this definition")
For a `dataclass` instance get the fields that are different from the default values and return as `dict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.SoftDollarTier.dict "ib_async.objects.SoftDollarTier.dict")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)"), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")]

tuple()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.SoftDollarTier.tuple "Link to this definition")
Return dataclass values as `tuple`. This is a non-recursive variant of `dataclasses.astuple`.

Return type:
[`tuple`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.SoftDollarTier.tuple "ib_async.objects.SoftDollarTier.tuple")[[`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)"), [`...`](https://docs.python.org/3/library/constants.html#Ellipsis "(in Python v3.14)")]

update(_*srcObjs_, _**kwargs_)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.SoftDollarTier.update "Link to this definition")
Update fields of the given `dataclass` object from zero or more `dataclass` source objects and/or from keyword arguments.

Return type:
[`object`](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)")

_class_ ib_async.objects.Execution(_execId=''_, _time=datetime.datetime(1970,1,1,0,0,tzinfo=datetime.timezone.utc)_, _acctNumber=''_, _exchange=''_, _side=''_, _shares=0.0_, _price=0.0_, _permId=0_, _clientId=0_, _orderId=0_, _liquidation=0_, _cumQty=0.0_, _avgPrice=0.0_, _orderRef=''_, _evRule=''_, _evMultiplier=0.0_, _modelCode=''_, _lastLiquidity=0_, _pendingPriceRevision=False_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/objects.html#Execution)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.Execution "Link to this definition")execId _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.Execution.execId "Link to this definition")time _:[`datetime`](https://docs.python.org/3/library/datetime.html#datetime.datetime "(in Python v3.14)")_ _=datetime.datetime(1970,1,1,0,0,tzinfo=datetime.timezone.utc)_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.Execution.time "Link to this definition")acctNumber _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.Execution.acctNumber "Link to this definition")exchange _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.Execution.exchange "Link to this definition")side _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.Execution.side "Link to this definition")shares _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=0.0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.Execution.shares "Link to this definition")price _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=0.0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.Execution.price "Link to this definition")permId _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.Execution.permId "Link to this definition")clientId _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.Execution.clientId "Link to this definition")orderId _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.Execution.orderId "Link to this definition")liquidation _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.Execution.liquidation "Link to this definition")cumQty _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=0.0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.Execution.cumQty "Link to this definition")avgPrice _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=0.0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.Execution.avgPrice "Link to this definition")orderRef _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.Execution.orderRef "Link to this definition")evRule _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.Execution.evRule "Link to this definition")evMultiplier _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=0.0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.Execution.evMultiplier "Link to this definition")modelCode _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.Execution.modelCode "Link to this definition")lastLiquidity _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.Execution.lastLiquidity "Link to this definition")pendingPriceRevision _:[`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")_ _=False_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.Execution.pendingPriceRevision "Link to this definition")dict()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.Execution.dict "Link to this definition")
Return dataclass values as `dict`. This is a non-recursive variant of `dataclasses.asdict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.Execution.dict "ib_async.objects.Execution.dict")

nonDefaults()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.Execution.nonDefaults "Link to this definition")
For a `dataclass` instance get the fields that are different from the default values and return as `dict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.Execution.dict "ib_async.objects.Execution.dict")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)"), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")]

tuple()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.Execution.tuple "Link to this definition")
Return dataclass values as `tuple`. This is a non-recursive variant of `dataclasses.astuple`.

Return type:
[`tuple`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.Execution.tuple "ib_async.objects.Execution.tuple")[[`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)"), [`...`](https://docs.python.org/3/library/constants.html#Ellipsis "(in Python v3.14)")]

update(_*srcObjs_, _**kwargs_)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.Execution.update "Link to this definition")
Update fields of the given `dataclass` object from zero or more `dataclass` source objects and/or from keyword arguments.

Return type:
[`object`](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)")

_class_ ib_async.objects.CommissionReport(_execId=''_, _commission=0.0_, _currency=''_, _realizedPNL=0.0_, _yield\_=0.0_, _yieldRedemptionDate=0_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/objects.html#CommissionReport)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.CommissionReport "Link to this definition")execId _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.CommissionReport.execId "Link to this definition")commission _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=0.0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.CommissionReport.commission "Link to this definition")currency _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.CommissionReport.currency "Link to this definition")realizedPNL _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=0.0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.CommissionReport.realizedPNL "Link to this definition")yield_ _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=0.0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.CommissionReport.yield_ "Link to this definition")yieldRedemptionDate _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.CommissionReport.yieldRedemptionDate "Link to this definition")dict()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.CommissionReport.dict "Link to this definition")
Return dataclass values as `dict`. This is a non-recursive variant of `dataclasses.asdict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.CommissionReport.dict "ib_async.objects.CommissionReport.dict")

nonDefaults()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.CommissionReport.nonDefaults "Link to this definition")
For a `dataclass` instance get the fields that are different from the default values and return as `dict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.CommissionReport.dict "ib_async.objects.CommissionReport.dict")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)"), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")]

tuple()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.CommissionReport.tuple "Link to this definition")
Return dataclass values as `tuple`. This is a non-recursive variant of `dataclasses.astuple`.

Return type:
[`tuple`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.CommissionReport.tuple "ib_async.objects.CommissionReport.tuple")[[`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)"), [`...`](https://docs.python.org/3/library/constants.html#Ellipsis "(in Python v3.14)")]

update(_*srcObjs_, _**kwargs_)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.CommissionReport.update "Link to this definition")
Update fields of the given `dataclass` object from zero or more `dataclass` source objects and/or from keyword arguments.

Return type:
[`object`](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)")

_class_ ib_async.objects.ExecutionFilter(_clientId=0_, _acctCode=''_, _time=''_, _symbol=''_, _secType=''_, _exchange=''_, _side=''_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/objects.html#ExecutionFilter)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.ExecutionFilter "Link to this definition")clientId _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.ExecutionFilter.clientId "Link to this definition")acctCode _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.ExecutionFilter.acctCode "Link to this definition")time _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.ExecutionFilter.time "Link to this definition")symbol _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.ExecutionFilter.symbol "Link to this definition")secType _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.ExecutionFilter.secType "Link to this definition")exchange _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.ExecutionFilter.exchange "Link to this definition")side _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.ExecutionFilter.side "Link to this definition")dict()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.ExecutionFilter.dict "Link to this definition")
Return dataclass values as `dict`. This is a non-recursive variant of `dataclasses.asdict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.ExecutionFilter.dict "ib_async.objects.ExecutionFilter.dict")

nonDefaults()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.ExecutionFilter.nonDefaults "Link to this definition")
For a `dataclass` instance get the fields that are different from the default values and return as `dict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.ExecutionFilter.dict "ib_async.objects.ExecutionFilter.dict")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)"), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")]

tuple()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.ExecutionFilter.tuple "Link to this definition")
Return dataclass values as `tuple`. This is a non-recursive variant of `dataclasses.astuple`.

Return type:
[`tuple`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.ExecutionFilter.tuple "ib_async.objects.ExecutionFilter.tuple")[[`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)"), [`...`](https://docs.python.org/3/library/constants.html#Ellipsis "(in Python v3.14)")]

update(_*srcObjs_, _**kwargs_)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.ExecutionFilter.update "Link to this definition")
Update fields of the given `dataclass` object from zero or more `dataclass` source objects and/or from keyword arguments.

Return type:
[`object`](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)")

_class_ ib_async.objects.BarData(_date=datetime.datetime(1970,1,1,0,0,tzinfo=datetime.timezone.utc)_, _open=0.0_, _high=0.0_, _low=0.0_, _close=0.0_, _volume=0_, _average=0.0_, _barCount=0_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/objects.html#BarData)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.BarData "Link to this definition")date _:[`date`](https://docs.python.org/3/library/datetime.html#datetime.date "(in Python v3.14)")|[`datetime`](https://docs.python.org/3/library/datetime.html#datetime.datetime "(in Python v3.14)")_ _=datetime.datetime(1970,1,1,0,0,tzinfo=datetime.timezone.utc)_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.BarData.date "Link to this definition")open _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=0.0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.BarData.open "Link to this definition")high _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=0.0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.BarData.high "Link to this definition")low _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=0.0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.BarData.low "Link to this definition")close _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=0.0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.BarData.close "Link to this definition")volume _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.BarData.volume "Link to this definition")average _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=0.0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.BarData.average "Link to this definition")barCount _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.BarData.barCount "Link to this definition")dict()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.BarData.dict "Link to this definition")
Return dataclass values as `dict`. This is a non-recursive variant of `dataclasses.asdict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.BarData.dict "ib_async.objects.BarData.dict")

nonDefaults()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.BarData.nonDefaults "Link to this definition")
For a `dataclass` instance get the fields that are different from the default values and return as `dict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.BarData.dict "ib_async.objects.BarData.dict")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)"), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")]

tuple()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.BarData.tuple "Link to this definition")
Return dataclass values as `tuple`. This is a non-recursive variant of `dataclasses.astuple`.

Return type:
[`tuple`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.BarData.tuple "ib_async.objects.BarData.tuple")[[`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)"), [`...`](https://docs.python.org/3/library/constants.html#Ellipsis "(in Python v3.14)")]

update(_*srcObjs_, _**kwargs_)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.BarData.update "Link to this definition")
Update fields of the given `dataclass` object from zero or more `dataclass` source objects and/or from keyword arguments.

Return type:
[`object`](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)")

_class_ ib_async.objects.RealTimeBar(_time=datetime.datetime(1970,1,1,0,0,tzinfo=datetime.timezone.utc)_, _endTime=-1_, _open\_=0.0_, _high=0.0_, _low=0.0_, _close=0.0_, _volume=0.0_, _wap=0.0_, _count=0_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/objects.html#RealTimeBar)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.RealTimeBar "Link to this definition")time _:[`datetime`](https://docs.python.org/3/library/datetime.html#datetime.datetime "(in Python v3.14)")_ _=datetime.datetime(1970,1,1,0,0,tzinfo=datetime.timezone.utc)_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.RealTimeBar.time "Link to this definition")endTime _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=-1_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.RealTimeBar.endTime "Link to this definition")open_ _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=0.0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.RealTimeBar.open_ "Link to this definition")high _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=0.0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.RealTimeBar.high "Link to this definition")low _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=0.0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.RealTimeBar.low "Link to this definition")close _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=0.0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.RealTimeBar.close "Link to this definition")volume _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=0.0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.RealTimeBar.volume "Link to this definition")wap _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=0.0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.RealTimeBar.wap "Link to this definition")count _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.RealTimeBar.count "Link to this definition")dict()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.RealTimeBar.dict "Link to this definition")
Return dataclass values as `dict`. This is a non-recursive variant of `dataclasses.asdict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.RealTimeBar.dict "ib_async.objects.RealTimeBar.dict")

nonDefaults()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.RealTimeBar.nonDefaults "Link to this definition")
For a `dataclass` instance get the fields that are different from the default values and return as `dict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.RealTimeBar.dict "ib_async.objects.RealTimeBar.dict")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)"), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")]

tuple()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.RealTimeBar.tuple "Link to this definition")
Return dataclass values as `tuple`. This is a non-recursive variant of `dataclasses.astuple`.

Return type:
[`tuple`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.RealTimeBar.tuple "ib_async.objects.RealTimeBar.tuple")[[`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)"), [`...`](https://docs.python.org/3/library/constants.html#Ellipsis "(in Python v3.14)")]

update(_*srcObjs_, _**kwargs_)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.RealTimeBar.update "Link to this definition")
Update fields of the given `dataclass` object from zero or more `dataclass` source objects and/or from keyword arguments.

Return type:
[`object`](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)")

_class_ ib_async.objects.TickAttrib(_canAutoExecute=False_, _pastLimit=False_, _preOpen=False_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/objects.html#TickAttrib)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.TickAttrib "Link to this definition")canAutoExecute _:[`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")_ _=False_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.TickAttrib.canAutoExecute "Link to this definition")pastLimit _:[`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")_ _=False_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.TickAttrib.pastLimit "Link to this definition")preOpen _:[`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")_ _=False_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.TickAttrib.preOpen "Link to this definition")dict()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.TickAttrib.dict "Link to this definition")
Return dataclass values as `dict`. This is a non-recursive variant of `dataclasses.asdict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.TickAttrib.dict "ib_async.objects.TickAttrib.dict")

nonDefaults()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.TickAttrib.nonDefaults "Link to this definition")
For a `dataclass` instance get the fields that are different from the default values and return as `dict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.TickAttrib.dict "ib_async.objects.TickAttrib.dict")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)"), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")]

tuple()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.TickAttrib.tuple "Link to this definition")
Return dataclass values as `tuple`. This is a non-recursive variant of `dataclasses.astuple`.

Return type:
[`tuple`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.TickAttrib.tuple "ib_async.objects.TickAttrib.tuple")[[`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)"), [`...`](https://docs.python.org/3/library/constants.html#Ellipsis "(in Python v3.14)")]

update(_*srcObjs_, _**kwargs_)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.TickAttrib.update "Link to this definition")
Update fields of the given `dataclass` object from zero or more `dataclass` source objects and/or from keyword arguments.

Return type:
[`object`](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)")

_class_ ib_async.objects.TickAttribBidAsk(_bidPastLow=False_, _askPastHigh=False_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/objects.html#TickAttribBidAsk)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.TickAttribBidAsk "Link to this definition")bidPastLow _:[`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")_ _=False_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.TickAttribBidAsk.bidPastLow "Link to this definition")askPastHigh _:[`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")_ _=False_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.TickAttribBidAsk.askPastHigh "Link to this definition")dict()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.TickAttribBidAsk.dict "Link to this definition")
Return dataclass values as `dict`. This is a non-recursive variant of `dataclasses.asdict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.TickAttribBidAsk.dict "ib_async.objects.TickAttribBidAsk.dict")

nonDefaults()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.TickAttribBidAsk.nonDefaults "Link to this definition")
For a `dataclass` instance get the fields that are different from the default values and return as `dict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.TickAttribBidAsk.dict "ib_async.objects.TickAttribBidAsk.dict")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)"), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")]

tuple()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.TickAttribBidAsk.tuple "Link to this definition")
Return dataclass values as `tuple`. This is a non-recursive variant of `dataclasses.astuple`.

Return type:
[`tuple`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.TickAttribBidAsk.tuple "ib_async.objects.TickAttribBidAsk.tuple")[[`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)"), [`...`](https://docs.python.org/3/library/constants.html#Ellipsis "(in Python v3.14)")]

update(_*srcObjs_, _**kwargs_)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.TickAttribBidAsk.update "Link to this definition")
Update fields of the given `dataclass` object from zero or more `dataclass` source objects and/or from keyword arguments.

Return type:
[`object`](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)")

_class_ ib_async.objects.TickAttribLast(_pastLimit=False_, _unreported=False_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/objects.html#TickAttribLast)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.TickAttribLast "Link to this definition")pastLimit _:[`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")_ _=False_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.TickAttribLast.pastLimit "Link to this definition")unreported _:[`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")_ _=False_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.TickAttribLast.unreported "Link to this definition")dict()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.TickAttribLast.dict "Link to this definition")
Return dataclass values as `dict`. This is a non-recursive variant of `dataclasses.asdict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.TickAttribLast.dict "ib_async.objects.TickAttribLast.dict")

nonDefaults()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.TickAttribLast.nonDefaults "Link to this definition")
For a `dataclass` instance get the fields that are different from the default values and return as `dict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.TickAttribLast.dict "ib_async.objects.TickAttribLast.dict")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)"), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")]

tuple()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.TickAttribLast.tuple "Link to this definition")
Return dataclass values as `tuple`. This is a non-recursive variant of `dataclasses.astuple`.

Return type:
[`tuple`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.TickAttribLast.tuple "ib_async.objects.TickAttribLast.tuple")[[`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)"), [`...`](https://docs.python.org/3/library/constants.html#Ellipsis "(in Python v3.14)")]

update(_*srcObjs_, _**kwargs_)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.TickAttribLast.update "Link to this definition")
Update fields of the given `dataclass` object from zero or more `dataclass` source objects and/or from keyword arguments.

Return type:
[`object`](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)")

_class_ ib_async.objects.HistogramData(_price=0.0_, _count=0_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/objects.html#HistogramData)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.HistogramData "Link to this definition")price _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=0.0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.HistogramData.price "Link to this definition")count _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.HistogramData.count "Link to this definition")dict()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.HistogramData.dict "Link to this definition")
Return dataclass values as `dict`. This is a non-recursive variant of `dataclasses.asdict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.HistogramData.dict "ib_async.objects.HistogramData.dict")

nonDefaults()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.HistogramData.nonDefaults "Link to this definition")
For a `dataclass` instance get the fields that are different from the default values and return as `dict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.HistogramData.dict "ib_async.objects.HistogramData.dict")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)"), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")]

tuple()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.HistogramData.tuple "Link to this definition")
Return dataclass values as `tuple`. This is a non-recursive variant of `dataclasses.astuple`.

Return type:
[`tuple`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.HistogramData.tuple "ib_async.objects.HistogramData.tuple")[[`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)"), [`...`](https://docs.python.org/3/library/constants.html#Ellipsis "(in Python v3.14)")]

update(_*srcObjs_, _**kwargs_)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.HistogramData.update "Link to this definition")
Update fields of the given `dataclass` object from zero or more `dataclass` source objects and/or from keyword arguments.

Return type:
[`object`](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)")

_class_ ib_async.objects.NewsProvider(_code=''_, _name=''_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/objects.html#NewsProvider)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.NewsProvider "Link to this definition")code _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.NewsProvider.code "Link to this definition")name _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.NewsProvider.name "Link to this definition")dict()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.NewsProvider.dict "Link to this definition")
Return dataclass values as `dict`. This is a non-recursive variant of `dataclasses.asdict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.NewsProvider.dict "ib_async.objects.NewsProvider.dict")

nonDefaults()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.NewsProvider.nonDefaults "Link to this definition")
For a `dataclass` instance get the fields that are different from the default values and return as `dict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.NewsProvider.dict "ib_async.objects.NewsProvider.dict")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)"), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")]

tuple()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.NewsProvider.tuple "Link to this definition")
Return dataclass values as `tuple`. This is a non-recursive variant of `dataclasses.astuple`.

Return type:
[`tuple`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.NewsProvider.tuple "ib_async.objects.NewsProvider.tuple")[[`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)"), [`...`](https://docs.python.org/3/library/constants.html#Ellipsis "(in Python v3.14)")]

update(_*srcObjs_, _**kwargs_)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.NewsProvider.update "Link to this definition")
Update fields of the given `dataclass` object from zero or more `dataclass` source objects and/or from keyword arguments.

Return type:
[`object`](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)")

_class_ ib_async.objects.DepthMktDataDescription(_exchange=''_, _secType=''_, _listingExch=''_, _serviceDataType=''_, _aggGroup=2147483647_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/objects.html#DepthMktDataDescription)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.DepthMktDataDescription "Link to this definition")exchange _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.DepthMktDataDescription.exchange "Link to this definition")secType _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.DepthMktDataDescription.secType "Link to this definition")listingExch _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.DepthMktDataDescription.listingExch "Link to this definition")serviceDataType _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.DepthMktDataDescription.serviceDataType "Link to this definition")aggGroup _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=2147483647_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.DepthMktDataDescription.aggGroup "Link to this definition")dict()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.DepthMktDataDescription.dict "Link to this definition")
Return dataclass values as `dict`. This is a non-recursive variant of `dataclasses.asdict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.DepthMktDataDescription.dict "ib_async.objects.DepthMktDataDescription.dict")

nonDefaults()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.DepthMktDataDescription.nonDefaults "Link to this definition")
For a `dataclass` instance get the fields that are different from the default values and return as `dict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.DepthMktDataDescription.dict "ib_async.objects.DepthMktDataDescription.dict")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)"), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")]

tuple()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.DepthMktDataDescription.tuple "Link to this definition")
Return dataclass values as `tuple`. This is a non-recursive variant of `dataclasses.astuple`.

Return type:
[`tuple`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.DepthMktDataDescription.tuple "ib_async.objects.DepthMktDataDescription.tuple")[[`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)"), [`...`](https://docs.python.org/3/library/constants.html#Ellipsis "(in Python v3.14)")]

update(_*srcObjs_, _**kwargs_)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.DepthMktDataDescription.update "Link to this definition")
Update fields of the given `dataclass` object from zero or more `dataclass` source objects and/or from keyword arguments.

Return type:
[`object`](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)")

_class_ ib_async.objects.PnL(_account=''_, _modelCode=''_, _dailyPnL=nan_, _unrealizedPnL=nan_, _realizedPnL=nan_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/objects.html#PnL)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.PnL "Link to this definition")account _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.PnL.account "Link to this definition")modelCode _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.PnL.modelCode "Link to this definition")dailyPnL _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.PnL.dailyPnL "Link to this definition")unrealizedPnL _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.PnL.unrealizedPnL "Link to this definition")realizedPnL _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.PnL.realizedPnL "Link to this definition")dict()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.PnL.dict "Link to this definition")
Return dataclass values as `dict`. This is a non-recursive variant of `dataclasses.asdict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.PnL.dict "ib_async.objects.PnL.dict")

nonDefaults()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.PnL.nonDefaults "Link to this definition")
For a `dataclass` instance get the fields that are different from the default values and return as `dict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.PnL.dict "ib_async.objects.PnL.dict")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)"), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")]

tuple()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.PnL.tuple "Link to this definition")
Return dataclass values as `tuple`. This is a non-recursive variant of `dataclasses.astuple`.

Return type:
[`tuple`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.PnL.tuple "ib_async.objects.PnL.tuple")[[`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)"), [`...`](https://docs.python.org/3/library/constants.html#Ellipsis "(in Python v3.14)")]

update(_*srcObjs_, _**kwargs_)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.PnL.update "Link to this definition")
Update fields of the given `dataclass` object from zero or more `dataclass` source objects and/or from keyword arguments.

Return type:
[`object`](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)")

_class_ ib_async.objects.TradeLogEntry(_time_, _status=''_, _message=''_, _errorCode=0_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/objects.html#TradeLogEntry)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.TradeLogEntry "Link to this definition")time _:[`datetime`](https://docs.python.org/3/library/datetime.html#datetime.datetime "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.TradeLogEntry.time "Link to this definition")status _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.TradeLogEntry.status "Link to this definition")message _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.TradeLogEntry.message "Link to this definition")errorCode _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.TradeLogEntry.errorCode "Link to this definition")dict()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.TradeLogEntry.dict "Link to this definition")
Return dataclass values as `dict`. This is a non-recursive variant of `dataclasses.asdict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.TradeLogEntry.dict "ib_async.objects.TradeLogEntry.dict")

nonDefaults()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.TradeLogEntry.nonDefaults "Link to this definition")
For a `dataclass` instance get the fields that are different from the default values and return as `dict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.TradeLogEntry.dict "ib_async.objects.TradeLogEntry.dict")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)"), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")]

tuple()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.TradeLogEntry.tuple "Link to this definition")
Return dataclass values as `tuple`. This is a non-recursive variant of `dataclasses.astuple`.

Return type:
[`tuple`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.TradeLogEntry.tuple "ib_async.objects.TradeLogEntry.tuple")[[`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)"), [`...`](https://docs.python.org/3/library/constants.html#Ellipsis "(in Python v3.14)")]

update(_*srcObjs_, _**kwargs_)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.TradeLogEntry.update "Link to this definition")
Update fields of the given `dataclass` object from zero or more `dataclass` source objects and/or from keyword arguments.

Return type:
[`object`](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)")

_class_ ib_async.objects.PnLSingle(_account=''_, _modelCode=''_, _conId=0_, _dailyPnL=nan_, _unrealizedPnL=nan_, _realizedPnL=nan_, _position=0_, _value=nan_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/objects.html#PnLSingle)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.PnLSingle "Link to this definition")account _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.PnLSingle.account "Link to this definition")modelCode _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.PnLSingle.modelCode "Link to this definition")conId _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.PnLSingle.conId "Link to this definition")dailyPnL _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.PnLSingle.dailyPnL "Link to this definition")unrealizedPnL _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.PnLSingle.unrealizedPnL "Link to this definition")realizedPnL _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.PnLSingle.realizedPnL "Link to this definition")position _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.PnLSingle.position "Link to this definition")value _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.PnLSingle.value "Link to this definition")dict()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.PnLSingle.dict "Link to this definition")
Return dataclass values as `dict`. This is a non-recursive variant of `dataclasses.asdict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.PnLSingle.dict "ib_async.objects.PnLSingle.dict")

nonDefaults()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.PnLSingle.nonDefaults "Link to this definition")
For a `dataclass` instance get the fields that are different from the default values and return as `dict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.PnLSingle.dict "ib_async.objects.PnLSingle.dict")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)"), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")]

tuple()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.PnLSingle.tuple "Link to this definition")
Return dataclass values as `tuple`. This is a non-recursive variant of `dataclasses.astuple`.

Return type:
[`tuple`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.PnLSingle.tuple "ib_async.objects.PnLSingle.tuple")[[`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)"), [`...`](https://docs.python.org/3/library/constants.html#Ellipsis "(in Python v3.14)")]

update(_*srcObjs_, _**kwargs_)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.PnLSingle.update "Link to this definition")
Update fields of the given `dataclass` object from zero or more `dataclass` source objects and/or from keyword arguments.

Return type:
[`object`](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)")

_class_ ib_async.objects.HistoricalSession(_startDateTime=''_, _endDateTime=''_, _refDate=''_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/objects.html#HistoricalSession)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.HistoricalSession "Link to this definition")startDateTime _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.HistoricalSession.startDateTime "Link to this definition")endDateTime _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.HistoricalSession.endDateTime "Link to this definition")refDate _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.HistoricalSession.refDate "Link to this definition")dict()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.HistoricalSession.dict "Link to this definition")
Return dataclass values as `dict`. This is a non-recursive variant of `dataclasses.asdict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.HistoricalSession.dict "ib_async.objects.HistoricalSession.dict")

nonDefaults()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.HistoricalSession.nonDefaults "Link to this definition")
For a `dataclass` instance get the fields that are different from the default values and return as `dict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.HistoricalSession.dict "ib_async.objects.HistoricalSession.dict")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)"), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")]

tuple()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.HistoricalSession.tuple "Link to this definition")
Return dataclass values as `tuple`. This is a non-recursive variant of `dataclasses.astuple`.

Return type:
[`tuple`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.HistoricalSession.tuple "ib_async.objects.HistoricalSession.tuple")[[`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)"), [`...`](https://docs.python.org/3/library/constants.html#Ellipsis "(in Python v3.14)")]

update(_*srcObjs_, _**kwargs_)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.HistoricalSession.update "Link to this definition")
Update fields of the given `dataclass` object from zero or more `dataclass` source objects and/or from keyword arguments.

Return type:
[`object`](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)")

_class_ ib_async.objects.HistoricalSchedule(_startDateTime=''_, _endDateTime=''_, _timeZone=''_, _sessions=<factory>_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/objects.html#HistoricalSchedule)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.HistoricalSchedule "Link to this definition")startDateTime _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.HistoricalSchedule.startDateTime "Link to this definition")endDateTime _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.HistoricalSchedule.endDateTime "Link to this definition")timeZone _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.HistoricalSchedule.timeZone "Link to this definition")sessions _:[`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`HistoricalSession`](https://ib-api-reloaded.github.io/ib\_async/api.html#ib\_async.objects.HistoricalSession "ib\_async.objects.HistoricalSession")]_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.HistoricalSchedule.sessions "Link to this definition")dict()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.HistoricalSchedule.dict "Link to this definition")
Return dataclass values as `dict`. This is a non-recursive variant of `dataclasses.asdict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.HistoricalSchedule.dict "ib_async.objects.HistoricalSchedule.dict")

nonDefaults()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.HistoricalSchedule.nonDefaults "Link to this definition")
For a `dataclass` instance get the fields that are different from the default values and return as `dict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.HistoricalSchedule.dict "ib_async.objects.HistoricalSchedule.dict")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)"), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")]

tuple()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.HistoricalSchedule.tuple "Link to this definition")
Return dataclass values as `tuple`. This is a non-recursive variant of `dataclasses.astuple`.

Return type:
[`tuple`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.HistoricalSchedule.tuple "ib_async.objects.HistoricalSchedule.tuple")[[`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)"), [`...`](https://docs.python.org/3/library/constants.html#Ellipsis "(in Python v3.14)")]

update(_*srcObjs_, _**kwargs_)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.HistoricalSchedule.update "Link to this definition")
Update fields of the given `dataclass` object from zero or more `dataclass` source objects and/or from keyword arguments.

Return type:
[`object`](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)")

_class_ ib_async.objects.WshEventData(_conId=2147483647_, _filter=''_, _fillWatchlist=False_, _fillPortfolio=False_, _fillCompetitors=False_, _startDate=''_, _endDate=''_, _totalLimit=2147483647_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/objects.html#WshEventData)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.WshEventData "Link to this definition")conId _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=2147483647_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.WshEventData.conId "Link to this definition")filter _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.WshEventData.filter "Link to this definition")fillWatchlist _:[`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")_ _=False_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.WshEventData.fillWatchlist "Link to this definition")fillPortfolio _:[`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")_ _=False_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.WshEventData.fillPortfolio "Link to this definition")fillCompetitors _:[`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")_ _=False_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.WshEventData.fillCompetitors "Link to this definition")startDate _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.WshEventData.startDate "Link to this definition")endDate _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.WshEventData.endDate "Link to this definition")totalLimit _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=2147483647_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.WshEventData.totalLimit "Link to this definition")dict()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.WshEventData.dict "Link to this definition")
Return dataclass values as `dict`. This is a non-recursive variant of `dataclasses.asdict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.WshEventData.dict "ib_async.objects.WshEventData.dict")

nonDefaults()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.WshEventData.nonDefaults "Link to this definition")
For a `dataclass` instance get the fields that are different from the default values and return as `dict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.WshEventData.dict "ib_async.objects.WshEventData.dict")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)"), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")]

tuple()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.WshEventData.tuple "Link to this definition")
Return dataclass values as `tuple`. This is a non-recursive variant of `dataclasses.astuple`.

Return type:
[`tuple`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.WshEventData.tuple "ib_async.objects.WshEventData.tuple")[[`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)"), [`...`](https://docs.python.org/3/library/constants.html#Ellipsis "(in Python v3.14)")]

update(_*srcObjs_, _**kwargs_)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.WshEventData.update "Link to this definition")
Update fields of the given `dataclass` object from zero or more `dataclass` source objects and/or from keyword arguments.

Return type:
[`object`](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)")

_class_ ib_async.objects.AccountValue(_account_, _tag_, _value_, _currency_, _modelCode_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/objects.html#AccountValue)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.AccountValue "Link to this definition")
Create new instance of AccountValue(account, tag, value, currency, modelCode)

account _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.AccountValue.account "Link to this definition")tag _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.AccountValue.tag "Link to this definition")value _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.AccountValue.value "Link to this definition")currency _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.AccountValue.currency "Link to this definition")modelCode _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.AccountValue.modelCode "Link to this definition")_class_ ib_async.objects.TickData(_time_, _tickType_, _price_, _size_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/objects.html#TickData)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.TickData "Link to this definition")
Create new instance of TickData(time, tickType, price, size)

time _:[`datetime`](https://docs.python.org/3/library/datetime.html#datetime.datetime "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.TickData.time "Link to this definition")tickType _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.TickData.tickType "Link to this definition")price _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.TickData.price "Link to this definition")size _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.TickData.size "Link to this definition")_class_ ib_async.objects.HistoricalTick(_time_, _price_, _size_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/objects.html#HistoricalTick)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.HistoricalTick "Link to this definition")
Create new instance of HistoricalTick(time, price, size)

time _:[`datetime`](https://docs.python.org/3/library/datetime.html#datetime.datetime "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.HistoricalTick.time "Link to this definition")price _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.HistoricalTick.price "Link to this definition")size _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.HistoricalTick.size "Link to this definition")_class_ ib_async.objects.HistoricalTickBidAsk(_time_, _tickAttribBidAsk_, _priceBid_, _priceAsk_, _sizeBid_, _sizeAsk_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/objects.html#HistoricalTickBidAsk)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.HistoricalTickBidAsk "Link to this definition")
Create new instance of HistoricalTickBidAsk(time, tickAttribBidAsk, priceBid, priceAsk, sizeBid, sizeAsk)

time _:[`datetime`](https://docs.python.org/3/library/datetime.html#datetime.datetime "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.HistoricalTickBidAsk.time "Link to this definition")tickAttribBidAsk _:[`TickAttribBidAsk`](https://ib-api-reloaded.github.io/ib\_async/api.html#ib\_async.objects.TickAttribBidAsk "ib\_async.objects.TickAttribBidAsk")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.HistoricalTickBidAsk.tickAttribBidAsk "Link to this definition")priceBid _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.HistoricalTickBidAsk.priceBid "Link to this definition")priceAsk _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.HistoricalTickBidAsk.priceAsk "Link to this definition")sizeBid _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.HistoricalTickBidAsk.sizeBid "Link to this definition")sizeAsk _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.HistoricalTickBidAsk.sizeAsk "Link to this definition")_class_ ib_async.objects.HistoricalTickLast(_time_, _tickAttribLast_, _price_, _size_, _exchange_, _specialConditions_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/objects.html#HistoricalTickLast)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.HistoricalTickLast "Link to this definition")
Create new instance of HistoricalTickLast(time, tickAttribLast, price, size, exchange, specialConditions)

time _:[`datetime`](https://docs.python.org/3/library/datetime.html#datetime.datetime "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.HistoricalTickLast.time "Link to this definition")tickAttribLast _:[`TickAttribLast`](https://ib-api-reloaded.github.io/ib\_async/api.html#ib\_async.objects.TickAttribLast "ib\_async.objects.TickAttribLast")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.HistoricalTickLast.tickAttribLast "Link to this definition")price _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.HistoricalTickLast.price "Link to this definition")size _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.HistoricalTickLast.size "Link to this definition")exchange _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.HistoricalTickLast.exchange "Link to this definition")specialConditions _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.HistoricalTickLast.specialConditions "Link to this definition")_class_ ib_async.objects.TickByTickAllLast(_tickType_, _time_, _price_, _size_, _tickAttribLast_, _exchange_, _specialConditions_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/objects.html#TickByTickAllLast)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.TickByTickAllLast "Link to this definition")
Create new instance of TickByTickAllLast(tickType, time, price, size, tickAttribLast, exchange, specialConditions)

tickType _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.TickByTickAllLast.tickType "Link to this definition")time _:[`datetime`](https://docs.python.org/3/library/datetime.html#datetime.datetime "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.TickByTickAllLast.time "Link to this definition")price _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.TickByTickAllLast.price "Link to this definition")size _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.TickByTickAllLast.size "Link to this definition")tickAttribLast _:[`TickAttribLast`](https://ib-api-reloaded.github.io/ib\_async/api.html#ib\_async.objects.TickAttribLast "ib\_async.objects.TickAttribLast")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.TickByTickAllLast.tickAttribLast "Link to this definition")exchange _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.TickByTickAllLast.exchange "Link to this definition")specialConditions _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.TickByTickAllLast.specialConditions "Link to this definition")_class_ ib_async.objects.TickByTickBidAsk(_time_, _bidPrice_, _askPrice_, _bidSize_, _askSize_, _tickAttribBidAsk_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/objects.html#TickByTickBidAsk)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.TickByTickBidAsk "Link to this definition")
Create new instance of TickByTickBidAsk(time, bidPrice, askPrice, bidSize, askSize, tickAttribBidAsk)

time _:[`datetime`](https://docs.python.org/3/library/datetime.html#datetime.datetime "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.TickByTickBidAsk.time "Link to this definition")bidPrice _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.TickByTickBidAsk.bidPrice "Link to this definition")askPrice _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.TickByTickBidAsk.askPrice "Link to this definition")bidSize _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.TickByTickBidAsk.bidSize "Link to this definition")askSize _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.TickByTickBidAsk.askSize "Link to this definition")tickAttribBidAsk _:[`TickAttribBidAsk`](https://ib-api-reloaded.github.io/ib\_async/api.html#ib\_async.objects.TickAttribBidAsk "ib\_async.objects.TickAttribBidAsk")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.TickByTickBidAsk.tickAttribBidAsk "Link to this definition")_class_ ib_async.objects.TickByTickMidPoint(_time_, _midPoint_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/objects.html#TickByTickMidPoint)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.TickByTickMidPoint "Link to this definition")
Create new instance of TickByTickMidPoint(time, midPoint)

time _:[`datetime`](https://docs.python.org/3/library/datetime.html#datetime.datetime "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.TickByTickMidPoint.time "Link to this definition")midPoint _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.TickByTickMidPoint.midPoint "Link to this definition")_class_ ib_async.objects.MktDepthData(_time_, _position_, _marketMaker_, _operation_, _side_, _price_, _size_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/objects.html#MktDepthData)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.MktDepthData "Link to this definition")
Create new instance of MktDepthData(time, position, marketMaker, operation, side, price, size)

time _:[`datetime`](https://docs.python.org/3/library/datetime.html#datetime.datetime "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.MktDepthData.time "Link to this definition")position _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.MktDepthData.position "Link to this definition")marketMaker _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.MktDepthData.marketMaker "Link to this definition")operation _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.MktDepthData.operation "Link to this definition")side _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.MktDepthData.side "Link to this definition")price _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.MktDepthData.price "Link to this definition")size _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.MktDepthData.size "Link to this definition")_class_ ib_async.objects.DOMLevel(_price_, _size_, _marketMaker_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/objects.html#DOMLevel)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.DOMLevel "Link to this definition")
Create new instance of DOMLevel(price, size, marketMaker)

price _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.DOMLevel.price "Link to this definition")size _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.DOMLevel.size "Link to this definition")marketMaker _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.DOMLevel.marketMaker "Link to this definition")_class_ ib_async.objects.PriceIncrement(_lowEdge_, _increment_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/objects.html#PriceIncrement)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.PriceIncrement "Link to this definition")
Create new instance of PriceIncrement(lowEdge, increment)

lowEdge _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.PriceIncrement.lowEdge "Link to this definition")increment _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.PriceIncrement.increment "Link to this definition")_class_ ib_async.objects.PortfolioItem(_contract_, _position_, _marketPrice_, _marketValue_, _averageCost_, _unrealizedPNL_, _realizedPNL_, _account_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/objects.html#PortfolioItem)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.PortfolioItem "Link to this definition")
Create new instance of PortfolioItem(contract, position, marketPrice, marketValue, averageCost, unrealizedPNL, realizedPNL, account)

contract _:[`Contract`](https://ib-api-reloaded.github.io/ib\_async/api.html#ib\_async.contract.Contract "ib\_async.contract.Contract")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.PortfolioItem.contract "Link to this definition")position _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.PortfolioItem.position "Link to this definition")marketPrice _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.PortfolioItem.marketPrice "Link to this definition")marketValue _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.PortfolioItem.marketValue "Link to this definition")averageCost _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.PortfolioItem.averageCost "Link to this definition")unrealizedPNL _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.PortfolioItem.unrealizedPNL "Link to this definition")realizedPNL _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.PortfolioItem.realizedPNL "Link to this definition")account _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.PortfolioItem.account "Link to this definition")_class_ ib_async.objects.Position(_account_, _contract_, _position_, _avgCost_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/objects.html#Position)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.Position "Link to this definition")
Create new instance of Position(account, contract, position, avgCost)

account _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.Position.account "Link to this definition")contract _:[`Contract`](https://ib-api-reloaded.github.io/ib\_async/api.html#ib\_async.contract.Contract "ib\_async.contract.Contract")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.Position.contract "Link to this definition")position _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.Position.position "Link to this definition")avgCost _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.Position.avgCost "Link to this definition")_class_ ib_async.objects.Fill(_contract_, _execution_, _commissionReport_, _time_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/objects.html#Fill)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.Fill "Link to this definition")
Create new instance of Fill(contract, execution, commissionReport, time)

contract _:[`Contract`](https://ib-api-reloaded.github.io/ib\_async/api.html#ib\_async.contract.Contract "ib\_async.contract.Contract")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.Fill.contract "Link to this definition")execution _:[`Execution`](https://ib-api-reloaded.github.io/ib\_async/api.html#ib\_async.objects.Execution "ib\_async.objects.Execution")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.Fill.execution "Link to this definition")commissionReport _:[`CommissionReport`](https://ib-api-reloaded.github.io/ib\_async/api.html#ib\_async.objects.CommissionReport "ib\_async.objects.CommissionReport")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.Fill.commissionReport "Link to this definition")time _:[`datetime`](https://docs.python.org/3/library/datetime.html#datetime.datetime "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.Fill.time "Link to this definition")_class_ ib_async.objects.EfpData(_basisPoints_, _formattedBasisPoints_, _impliedFuture_, _holdDays_, _futureLastTradeDate_, _dividendImpact_, _dividendsToLastTradeDate_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/objects.html#EfpData)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.EfpData "Link to this definition")
Exchange for Physical (EFP) futures data.

EFP allows trading a position in a single stock for a position in the corresponding single stock future.

basisPoints _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.EfpData.basisPoints "Link to this definition")formattedBasisPoints _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.EfpData.formattedBasisPoints "Link to this definition")impliedFuture _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.EfpData.impliedFuture "Link to this definition")holdDays _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.EfpData.holdDays "Link to this definition")futureLastTradeDate _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.EfpData.futureLastTradeDate "Link to this definition")dividendImpact _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.EfpData.dividendImpact "Link to this definition")dividendsToLastTradeDate _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.EfpData.dividendsToLastTradeDate "Link to this definition")_class_ ib_async.objects.OptionComputation(_tickAttrib_, _impliedVol=None_, _delta=None_, _optPrice=None_, _pvDividend=None_, _gamma=None_, _vega=None_, _theta=None_, _undPrice=None_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/objects.html#OptionComputation)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.OptionComputation "Link to this definition")tickAttrib _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.OptionComputation.tickAttrib "Link to this definition")impliedVol _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")|[`None`](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.OptionComputation.impliedVol "Link to this definition")delta _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")|[`None`](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.OptionComputation.delta "Link to this definition")optPrice _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")|[`None`](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.OptionComputation.optPrice "Link to this definition")pvDividend _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")|[`None`](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.OptionComputation.pvDividend "Link to this definition")gamma _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")|[`None`](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.OptionComputation.gamma "Link to this definition")vega _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")|[`None`](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.OptionComputation.vega "Link to this definition")theta _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")|[`None`](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.OptionComputation.theta "Link to this definition")undPrice _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")|[`None`](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.OptionComputation.undPrice "Link to this definition")dict()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.OptionComputation.dict "Link to this definition")
Return dataclass values as `dict`. This is a non-recursive variant of `dataclasses.asdict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.OptionComputation.dict "ib_async.objects.OptionComputation.dict")

nonDefaults()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.OptionComputation.nonDefaults "Link to this definition")
For a `dataclass` instance get the fields that are different from the default values and return as `dict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.OptionComputation.dict "ib_async.objects.OptionComputation.dict")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)"), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")]

tuple()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.OptionComputation.tuple "Link to this definition")
Return dataclass values as `tuple`. This is a non-recursive variant of `dataclasses.astuple`.

Return type:
[`tuple`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.OptionComputation.tuple "ib_async.objects.OptionComputation.tuple")[[`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)"), [`...`](https://docs.python.org/3/library/constants.html#Ellipsis "(in Python v3.14)")]

update(_*srcObjs_, _**kwargs_)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.OptionComputation.update "Link to this definition")
Update fields of the given `dataclass` object from zero or more `dataclass` source objects and/or from keyword arguments.

Return type:
[`object`](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)")

_class_ ib_async.objects.OptionChain(_exchange_, _underlyingConId_, _tradingClass_, _multiplier_, _expirations_, _strikes_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/objects.html#OptionChain)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.OptionChain "Link to this definition")exchange _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.OptionChain.exchange "Link to this definition")underlyingConId _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.OptionChain.underlyingConId "Link to this definition")tradingClass _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.OptionChain.tradingClass "Link to this definition")multiplier _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.OptionChain.multiplier "Link to this definition")expirations _:[`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")]_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.OptionChain.expirations "Link to this definition")strikes _:[`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")]_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.OptionChain.strikes "Link to this definition")dict()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.OptionChain.dict "Link to this definition")
Return dataclass values as `dict`. This is a non-recursive variant of `dataclasses.asdict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.OptionChain.dict "ib_async.objects.OptionChain.dict")

nonDefaults()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.OptionChain.nonDefaults "Link to this definition")
For a `dataclass` instance get the fields that are different from the default values and return as `dict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.OptionChain.dict "ib_async.objects.OptionChain.dict")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)"), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")]

tuple()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.OptionChain.tuple "Link to this definition")
Return dataclass values as `tuple`. This is a non-recursive variant of `dataclasses.astuple`.

Return type:
[`tuple`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.OptionChain.tuple "ib_async.objects.OptionChain.tuple")[[`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)"), [`...`](https://docs.python.org/3/library/constants.html#Ellipsis "(in Python v3.14)")]

update(_*srcObjs_, _**kwargs_)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.OptionChain.update "Link to this definition")
Update fields of the given `dataclass` object from zero or more `dataclass` source objects and/or from keyword arguments.

Return type:
[`object`](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)")

_class_ ib_async.objects.Dividends(_past12Months_, _next12Months_, _nextDate_, _nextAmount_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/objects.html#Dividends)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.Dividends "Link to this definition")past12Months _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")|[`None`](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.Dividends.past12Months "Link to this definition")next12Months _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")|[`None`](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.Dividends.next12Months "Link to this definition")nextDate _:[`date`](https://docs.python.org/3/library/datetime.html#datetime.date "(in Python v3.14)")|[`None`](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.Dividends.nextDate "Link to this definition")nextAmount _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")|[`None`](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.Dividends.nextAmount "Link to this definition")dict()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.Dividends.dict "Link to this definition")
Return dataclass values as `dict`. This is a non-recursive variant of `dataclasses.asdict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.Dividends.dict "ib_async.objects.Dividends.dict")

nonDefaults()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.Dividends.nonDefaults "Link to this definition")
For a `dataclass` instance get the fields that are different from the default values and return as `dict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.Dividends.dict "ib_async.objects.Dividends.dict")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)"), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")]

tuple()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.Dividends.tuple "Link to this definition")
Return dataclass values as `tuple`. This is a non-recursive variant of `dataclasses.astuple`.

Return type:
[`tuple`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.Dividends.tuple "ib_async.objects.Dividends.tuple")[[`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)"), [`...`](https://docs.python.org/3/library/constants.html#Ellipsis "(in Python v3.14)")]

update(_*srcObjs_, _**kwargs_)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.Dividends.update "Link to this definition")
Update fields of the given `dataclass` object from zero or more `dataclass` source objects and/or from keyword arguments.

Return type:
[`object`](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)")

_class_ ib_async.objects.NewsArticle(_articleType_, _articleText_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/objects.html#NewsArticle)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.NewsArticle "Link to this definition")articleType _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.NewsArticle.articleType "Link to this definition")articleText _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.NewsArticle.articleText "Link to this definition")dict()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.NewsArticle.dict "Link to this definition")
Return dataclass values as `dict`. This is a non-recursive variant of `dataclasses.asdict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.NewsArticle.dict "ib_async.objects.NewsArticle.dict")

nonDefaults()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.NewsArticle.nonDefaults "Link to this definition")
For a `dataclass` instance get the fields that are different from the default values and return as `dict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.NewsArticle.dict "ib_async.objects.NewsArticle.dict")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)"), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")]

tuple()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.NewsArticle.tuple "Link to this definition")
Return dataclass values as `tuple`. This is a non-recursive variant of `dataclasses.astuple`.

Return type:
[`tuple`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.NewsArticle.tuple "ib_async.objects.NewsArticle.tuple")[[`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)"), [`...`](https://docs.python.org/3/library/constants.html#Ellipsis "(in Python v3.14)")]

update(_*srcObjs_, _**kwargs_)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.NewsArticle.update "Link to this definition")
Update fields of the given `dataclass` object from zero or more `dataclass` source objects and/or from keyword arguments.

Return type:
[`object`](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)")

_class_ ib_async.objects.HistoricalNews(_time_, _providerCode_, _articleId_, _headline_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/objects.html#HistoricalNews)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.HistoricalNews "Link to this definition")time _:[`datetime`](https://docs.python.org/3/library/datetime.html#datetime.datetime "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.HistoricalNews.time "Link to this definition")providerCode _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.HistoricalNews.providerCode "Link to this definition")articleId _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.HistoricalNews.articleId "Link to this definition")headline _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.HistoricalNews.headline "Link to this definition")dict()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.HistoricalNews.dict "Link to this definition")
Return dataclass values as `dict`. This is a non-recursive variant of `dataclasses.asdict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.HistoricalNews.dict "ib_async.objects.HistoricalNews.dict")

nonDefaults()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.HistoricalNews.nonDefaults "Link to this definition")
For a `dataclass` instance get the fields that are different from the default values and return as `dict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.HistoricalNews.dict "ib_async.objects.HistoricalNews.dict")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)"), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")]

tuple()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.HistoricalNews.tuple "Link to this definition")
Return dataclass values as `tuple`. This is a non-recursive variant of `dataclasses.astuple`.

Return type:
[`tuple`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.HistoricalNews.tuple "ib_async.objects.HistoricalNews.tuple")[[`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)"), [`...`](https://docs.python.org/3/library/constants.html#Ellipsis "(in Python v3.14)")]

update(_*srcObjs_, _**kwargs_)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.HistoricalNews.update "Link to this definition")
Update fields of the given `dataclass` object from zero or more `dataclass` source objects and/or from keyword arguments.

Return type:
[`object`](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)")

_class_ ib_async.objects.NewsTick(_timeStamp_, _providerCode_, _articleId_, _headline_, _extraData_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/objects.html#NewsTick)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.NewsTick "Link to this definition")timeStamp _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.NewsTick.timeStamp "Link to this definition")providerCode _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.NewsTick.providerCode "Link to this definition")articleId _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.NewsTick.articleId "Link to this definition")headline _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.NewsTick.headline "Link to this definition")extraData _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.NewsTick.extraData "Link to this definition")dict()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.NewsTick.dict "Link to this definition")
Return dataclass values as `dict`. This is a non-recursive variant of `dataclasses.asdict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.NewsTick.dict "ib_async.objects.NewsTick.dict")

nonDefaults()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.NewsTick.nonDefaults "Link to this definition")
For a `dataclass` instance get the fields that are different from the default values and return as `dict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.NewsTick.dict "ib_async.objects.NewsTick.dict")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)"), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")]

tuple()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.NewsTick.tuple "Link to this definition")
Return dataclass values as `tuple`. This is a non-recursive variant of `dataclasses.astuple`.

Return type:
[`tuple`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.NewsTick.tuple "ib_async.objects.NewsTick.tuple")[[`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)"), [`...`](https://docs.python.org/3/library/constants.html#Ellipsis "(in Python v3.14)")]

update(_*srcObjs_, _**kwargs_)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.NewsTick.update "Link to this definition")
Update fields of the given `dataclass` object from zero or more `dataclass` source objects and/or from keyword arguments.

Return type:
[`object`](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)")

_class_ ib_async.objects.NewsBulletin(_msgId_, _msgType_, _message_, _origExchange_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/objects.html#NewsBulletin)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.NewsBulletin "Link to this definition")msgId _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.NewsBulletin.msgId "Link to this definition")msgType _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.NewsBulletin.msgType "Link to this definition")message _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.NewsBulletin.message "Link to this definition")origExchange _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.NewsBulletin.origExchange "Link to this definition")dict()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.NewsBulletin.dict "Link to this definition")
Return dataclass values as `dict`. This is a non-recursive variant of `dataclasses.asdict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.NewsBulletin.dict "ib_async.objects.NewsBulletin.dict")

nonDefaults()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.NewsBulletin.nonDefaults "Link to this definition")
For a `dataclass` instance get the fields that are different from the default values and return as `dict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.NewsBulletin.dict "ib_async.objects.NewsBulletin.dict")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)"), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")]

tuple()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.NewsBulletin.tuple "Link to this definition")
Return dataclass values as `tuple`. This is a non-recursive variant of `dataclasses.astuple`.

Return type:
[`tuple`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.NewsBulletin.tuple "ib_async.objects.NewsBulletin.tuple")[[`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)"), [`...`](https://docs.python.org/3/library/constants.html#Ellipsis "(in Python v3.14)")]

update(_*srcObjs_, _**kwargs_)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.NewsBulletin.update "Link to this definition")
Update fields of the given `dataclass` object from zero or more `dataclass` source objects and/or from keyword arguments.

Return type:
[`object`](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)")

_class_ ib_async.objects.FamilyCode(_accountID_, _familyCodeStr_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/objects.html#FamilyCode)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.FamilyCode "Link to this definition")accountID _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.FamilyCode.accountID "Link to this definition")familyCodeStr _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.FamilyCode.familyCodeStr "Link to this definition")dict()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.FamilyCode.dict "Link to this definition")
Return dataclass values as `dict`. This is a non-recursive variant of `dataclasses.asdict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.FamilyCode.dict "ib_async.objects.FamilyCode.dict")

nonDefaults()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.FamilyCode.nonDefaults "Link to this definition")
For a `dataclass` instance get the fields that are different from the default values and return as `dict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.FamilyCode.dict "ib_async.objects.FamilyCode.dict")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)"), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")]

tuple()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.FamilyCode.tuple "Link to this definition")
Return dataclass values as `tuple`. This is a non-recursive variant of `dataclasses.astuple`.

Return type:
[`tuple`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.FamilyCode.tuple "ib_async.objects.FamilyCode.tuple")[[`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)"), [`...`](https://docs.python.org/3/library/constants.html#Ellipsis "(in Python v3.14)")]

update(_*srcObjs_, _**kwargs_)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.FamilyCode.update "Link to this definition")
Update fields of the given `dataclass` object from zero or more `dataclass` source objects and/or from keyword arguments.

Return type:
[`object`](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)")

_class_ ib_async.objects.SmartComponent(_bitNumber_, _exchange_, _exchangeLetter_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/objects.html#SmartComponent)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.SmartComponent "Link to this definition")bitNumber _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.SmartComponent.bitNumber "Link to this definition")exchange _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.SmartComponent.exchange "Link to this definition")exchangeLetter _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.SmartComponent.exchangeLetter "Link to this definition")dict()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.SmartComponent.dict "Link to this definition")
Return dataclass values as `dict`. This is a non-recursive variant of `dataclasses.asdict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.SmartComponent.dict "ib_async.objects.SmartComponent.dict")

nonDefaults()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.SmartComponent.nonDefaults "Link to this definition")
For a `dataclass` instance get the fields that are different from the default values and return as `dict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.SmartComponent.dict "ib_async.objects.SmartComponent.dict")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)"), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")]

tuple()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.SmartComponent.tuple "Link to this definition")
Return dataclass values as `tuple`. This is a non-recursive variant of `dataclasses.astuple`.

Return type:
[`tuple`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.SmartComponent.tuple "ib_async.objects.SmartComponent.tuple")[[`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)"), [`...`](https://docs.python.org/3/library/constants.html#Ellipsis "(in Python v3.14)")]

update(_*srcObjs_, _**kwargs_)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.SmartComponent.update "Link to this definition")
Update fields of the given `dataclass` object from zero or more `dataclass` source objects and/or from keyword arguments.

Return type:
[`object`](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)")

_class_ ib_async.objects.ConnectionStats(_startTime_, _duration_, _numBytesRecv_, _numBytesSent_, _numMsgRecv_, _numMsgSent_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/objects.html#ConnectionStats)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.ConnectionStats "Link to this definition")startTime _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.ConnectionStats.startTime "Link to this definition")duration _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.ConnectionStats.duration "Link to this definition")numBytesRecv _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.ConnectionStats.numBytesRecv "Link to this definition")numBytesSent _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.ConnectionStats.numBytesSent "Link to this definition")numMsgRecv _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.ConnectionStats.numMsgRecv "Link to this definition")numMsgSent _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.ConnectionStats.numMsgSent "Link to this definition")dict()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.ConnectionStats.dict "Link to this definition")
Return dataclass values as `dict`. This is a non-recursive variant of `dataclasses.asdict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.ConnectionStats.dict "ib_async.objects.ConnectionStats.dict")

nonDefaults()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.ConnectionStats.nonDefaults "Link to this definition")
For a `dataclass` instance get the fields that are different from the default values and return as `dict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.ConnectionStats.dict "ib_async.objects.ConnectionStats.dict")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)"), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")]

tuple()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.ConnectionStats.tuple "Link to this definition")
Return dataclass values as `tuple`. This is a non-recursive variant of `dataclasses.astuple`.

Return type:
[`tuple`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.ConnectionStats.tuple "ib_async.objects.ConnectionStats.tuple")[[`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)"), [`...`](https://docs.python.org/3/library/constants.html#Ellipsis "(in Python v3.14)")]

update(_*srcObjs_, _**kwargs_)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.ConnectionStats.update "Link to this definition")
Update fields of the given `dataclass` object from zero or more `dataclass` source objects and/or from keyword arguments.

Return type:
[`object`](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)")

_class_ ib_async.objects.BarDataList(_*args_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/objects.html#BarDataList)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.BarDataList "Link to this definition")
List of [`BarData`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.BarData "ib_async.objects.BarData") that also stores all request parameters.

Events:

> *   `updateEvent` (bars: [`BarDataList`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.BarDataList "ib_async.objects.BarDataList"), hasNewBar: bool)

reqId _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.BarDataList.reqId "Link to this definition")contract _:[`Contract`](https://ib-api-reloaded.github.io/ib\_async/api.html#ib\_async.contract.Contract "ib\_async.contract.Contract")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.BarDataList.contract "Link to this definition")endDateTime _:[`datetime`](https://docs.python.org/3/library/datetime.html#datetime.datetime "(in Python v3.14)")|[`date`](https://docs.python.org/3/library/datetime.html#datetime.date "(in Python v3.14)")|[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")|[`None`](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.BarDataList.endDateTime "Link to this definition")durationStr _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.BarDataList.durationStr "Link to this definition")barSizeSetting _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.BarDataList.barSizeSetting "Link to this definition")whatToShow _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.BarDataList.whatToShow "Link to this definition")useRTH _:[`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.BarDataList.useRTH "Link to this definition")formatDate _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.BarDataList.formatDate "Link to this definition")keepUpToDate _:[`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.BarDataList.keepUpToDate "Link to this definition")chartOptions _:[`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`TagValue`](https://ib-api-reloaded.github.io/ib\_async/api.html#ib\_async.contract.TagValue "ib\_async.contract.TagValue")]_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.BarDataList.chartOptions "Link to this definition")_class_ ib_async.objects.RealTimeBarList(_*args_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/objects.html#RealTimeBarList)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.RealTimeBarList "Link to this definition")
List of [`RealTimeBar`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.RealTimeBar "ib_async.objects.RealTimeBar") that also stores all request parameters.

Events:

> *   `updateEvent` (bars: [`RealTimeBarList`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.RealTimeBarList "ib_async.objects.RealTimeBarList"), hasNewBar: bool)

reqId _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.RealTimeBarList.reqId "Link to this definition")contract _:[`Contract`](https://ib-api-reloaded.github.io/ib\_async/api.html#ib\_async.contract.Contract "ib\_async.contract.Contract")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.RealTimeBarList.contract "Link to this definition")barSize _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.RealTimeBarList.barSize "Link to this definition")whatToShow _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.RealTimeBarList.whatToShow "Link to this definition")useRTH _:[`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.RealTimeBarList.useRTH "Link to this definition")realTimeBarsOptions _:[`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`TagValue`](https://ib-api-reloaded.github.io/ib\_async/api.html#ib\_async.contract.TagValue "ib\_async.contract.TagValue")]_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.RealTimeBarList.realTimeBarsOptions "Link to this definition")_class_ ib_async.objects.ScanDataList(_*args_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/objects.html#ScanDataList)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.ScanDataList "Link to this definition")
List of [`ScanData`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.ScanData "ib_async.contract.ScanData") that also stores all request parameters.

Events:
*   `updateEvent` ([`ScanDataList`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.ScanDataList "ib_async.objects.ScanDataList"))

reqId _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.ScanDataList.reqId "Link to this definition")subscription _:[`ScannerSubscription`](https://ib-api-reloaded.github.io/ib\_async/api.html#ib\_async.objects.ScannerSubscription "ib\_async.objects.ScannerSubscription")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.ScanDataList.subscription "Link to this definition")scannerSubscriptionOptions _:[`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`TagValue`](https://ib-api-reloaded.github.io/ib\_async/api.html#ib\_async.contract.TagValue "ib\_async.contract.TagValue")]_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.ScanDataList.scannerSubscriptionOptions "Link to this definition")scannerSubscriptionFilterOptions _:[`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`TagValue`](https://ib-api-reloaded.github.io/ib\_async/api.html#ib\_async.contract.TagValue "ib\_async.contract.TagValue")]_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.ScanDataList.scannerSubscriptionFilterOptions "Link to this definition")_class_ ib_async.objects.DynamicObject(_**kwargs_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/objects.html#DynamicObject)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.DynamicObject "Link to this definition")_class_ ib_async.objects.FundamentalRatios(_**kwargs_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/objects.html#FundamentalRatios)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.FundamentalRatios "Link to this definition")
See: [https://web.archive.org/web/20200725010343/https://interactivebrokers.github.io/tws-api/fundamental_ratios_tags.html](https://web.archive.org/web/20200725010343/https://interactivebrokers.github.io/tws-api/fundamental_ratios_tags.html)

_class_ ib_async.objects.IBDefaults(_emptyPrice=-1_, _emptySize=0_, _unset=nan_, _timezone=datetime.timezone.utc_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/objects.html#IBDefaults)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.IBDefaults "Link to this definition")
A simple way to provide default values when populating API data.

emptyPrice _:[`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")_ _=-1_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.IBDefaults.emptyPrice "Link to this definition")emptySize _:[`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")_ _=0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.IBDefaults.emptySize "Link to this definition")unset _:[`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")_ _=nan_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.IBDefaults.unset "Link to this definition")timezone _:[`tzinfo`](https://docs.python.org/3/library/datetime.html#datetime.tzinfo "(in Python v3.14)")_ _=datetime.timezone.utc_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.IBDefaults.timezone "Link to this definition")dict()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.IBDefaults.dict "Link to this definition")
Return dataclass values as `dict`. This is a non-recursive variant of `dataclasses.asdict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.IBDefaults.dict "ib_async.objects.IBDefaults.dict")

nonDefaults()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.IBDefaults.nonDefaults "Link to this definition")
For a `dataclass` instance get the fields that are different from the default values and return as `dict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.IBDefaults.dict "ib_async.objects.IBDefaults.dict")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)"), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")]

tuple()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.IBDefaults.tuple "Link to this definition")
Return dataclass values as `tuple`. This is a non-recursive variant of `dataclasses.astuple`.

Return type:
[`tuple`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.IBDefaults.tuple "ib_async.objects.IBDefaults.tuple")[[`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)"), [`...`](https://docs.python.org/3/library/constants.html#Ellipsis "(in Python v3.14)")]

update(_*srcObjs_, _**kwargs_)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.objects.IBDefaults.update "Link to this definition")
Update fields of the given `dataclass` object from zero or more `dataclass` source objects and/or from keyword arguments.

Return type:
[`object`](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)")

_class_ ib_async.wrapper.RequestError(_reqId_, _code_, _message_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/wrapper.html#RequestError)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.wrapper.RequestError "Link to this definition")
Exception to raise when the API reports an error that can be tied to a single request.

Parameters:
*   **reqId** ([`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) – Original request ID.

*   **code** ([`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) – Original error code.

*   **message** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – Original error message.

Utilities[](https://ib-api-reloaded.github.io/ib_async/api.html#module-ib_async.util "Link to this heading")
-------------------------------------------------------------------------------------------------------------

Utilities.

ib_async.util.globalErrorEvent(_*args_)_=Event<Event,Slots(slots=[])>_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.util.globalErrorEvent "Link to this definition")
Event to emit global exceptions.

ib_async.util.df(_objs_, _labels=None_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/util.html#df)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.util.df "Link to this definition")
Create pandas DataFrame from the sequence of same-type objects.

Parameters:
**labels** ([`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")] | [`None`](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")) – If supplied, retain only the given labels and drop the rest.

ib_async.util.dataclassAsDict(_obj_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/util.html#dataclassAsDict)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.util.dataclassAsDict "Link to this definition")
Return dataclass values as `dict`. This is a non-recursive variant of `dataclasses.asdict`.

Return type:
[`dict`](https://docs.python.org/3/library/stdtypes.html#dict "(in Python v3.14)")

ib_async.util.dataclassAsTuple(_obj_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/util.html#dataclassAsTuple)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.util.dataclassAsTuple "Link to this definition")
Return dataclass values as `tuple`. This is a non-recursive variant of `dataclasses.astuple`.

Return type:
[`tuple`](https://docs.python.org/3/library/stdtypes.html#tuple "(in Python v3.14)")[[`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)"), [`...`](https://docs.python.org/3/library/constants.html#Ellipsis "(in Python v3.14)")]

ib_async.util.dataclassNonDefaults(_obj_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/util.html#dataclassNonDefaults)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.util.dataclassNonDefaults "Link to this definition")
For a `dataclass` instance get the fields that are different from the default values and return as `dict`.

Return type:
[`dict`](https://docs.python.org/3/library/stdtypes.html#dict "(in Python v3.14)")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)"), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")]

ib_async.util.dataclassUpdate(_obj_, _*srcObjs_, _**kwargs_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/util.html#dataclassUpdate)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.util.dataclassUpdate "Link to this definition")
Update fields of the given `dataclass` object from zero or more `dataclass` source objects and/or from keyword arguments.

Return type:
[`object`](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)")

ib_async.util.dataclassRepr(_obj_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/util.html#dataclassRepr)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.util.dataclassRepr "Link to this definition")
Provide a culled representation of the given `dataclass` instance, showing only the fields with a non-default value.

Return type:
[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")

ib_async.util.isnamedtupleinstance(_x_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/util.html#isnamedtupleinstance)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.util.isnamedtupleinstance "Link to this definition")
From [https://stackoverflow.com/a/2166841/6067848](https://stackoverflow.com/a/2166841/6067848)

ib_async.util.tree(_obj_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/util.html#tree)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.util.tree "Link to this definition")
Convert object to a tree of lists, dicts and simple values. The result can be serialized to JSON.

ib_async.util.barplot(_bars_, _title=''_, _upColor='blue'_, _downColor='red'_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/util.html#barplot)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.util.barplot "Link to this definition")
Create candlestick plot for the given bars. The bars can be given as a DataFrame or as a list of bar objects.

ib_async.util.allowCtrlC()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/util.html#allowCtrlC)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.util.allowCtrlC "Link to this definition")
Allow Control-C to end program.

ib_async.util.logToFile(_path_, _level=20_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/util.html#logToFile)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.util.logToFile "Link to this definition")
Create a log handler that logs to the given file.

ib_async.util.logToConsole(_level=20_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/util.html#logToConsole)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.util.logToConsole "Link to this definition")
Create a log handler that logs to the console.

ib_async.util.isNan(_x_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/util.html#isNan)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.util.isNan "Link to this definition")
Not a number test.

Return type:
[`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")

ib_async.util.formatSI(_n_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/util.html#formatSI)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.util.formatSI "Link to this definition")
Format the integer or float n to 3 significant digits + SI prefix.

Return type:
[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")

_class_ ib_async.util.timeit(_title='Run'_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/util.html#timeit)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.util.timeit "Link to this definition")
Context manager for timing.

ib_async.util.run(_*awaitables_, _timeout=None_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/util.html#run)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.util.run "Link to this definition")
By default run the event loop forever.

When awaitables (like Tasks, Futures or coroutines) are given then run the event loop until each has completed and return their results.

An optional timeout (in seconds) can be given that will raise asyncio.TimeoutError if the awaitables are not ready within the timeout period.

ib_async.util.schedule(_time_, _callback_, _*args_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/util.html#schedule)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.util.schedule "Link to this definition")
Schedule the callback to be run at the given time with the given arguments. This will return the Event Handle.

Parameters:
*   **time** ([`time`](https://docs.python.org/3/library/datetime.html#datetime.time "(in Python v3.14)") | [`datetime`](https://docs.python.org/3/library/datetime.html#datetime.datetime "(in Python v3.14)")) – Time to run callback. If given as [`datetime.time`](https://docs.python.org/3/library/datetime.html#datetime.time "(in Python v3.14)") then use today as date.

*   **callback** ([`Callable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Callable "(in Python v3.14)")) – Callable scheduled to run.

*   **args** – Arguments for to call callback with.

ib_async.util.sleep(_secs=0.02_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/util.html#sleep)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.util.sleep "Link to this definition")
Wait for the given amount of seconds while everything still keeps processing in the background. Never use time.sleep().

Parameters:
**secs** ([_float_](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")) – Time in seconds to wait.

Return type:
[`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")

ib_async.util.timeRange(_start_, _end_, _step_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/util.html#timeRange)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.util.timeRange "Link to this definition")
Iterator that waits periodically until certain time points are reached while yielding those time points.

Parameters:
*   **start** ([`time`](https://docs.python.org/3/library/datetime.html#datetime.time "(in Python v3.14)") | [`datetime`](https://docs.python.org/3/library/datetime.html#datetime.datetime "(in Python v3.14)")) – Start time, can be specified as datetime.datetime, or as datetime.time in which case today is used as the date

*   **end** ([`time`](https://docs.python.org/3/library/datetime.html#datetime.time "(in Python v3.14)") | [`datetime`](https://docs.python.org/3/library/datetime.html#datetime.datetime "(in Python v3.14)")) – End time, can be specified as datetime.datetime, or as datetime.time in which case today is used as the date

*   **step** ([_float_](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")) – The number of seconds of each period

Return type:
[`Iterator`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Iterator "(in Python v3.14)")[[`datetime`](https://docs.python.org/3/library/datetime.html#datetime.datetime "(in Python v3.14)")]

ib_async.util.waitUntil(_t_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/util.html#waitUntil)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.util.waitUntil "Link to this definition")
Wait until the given time t is reached.

Parameters:
**t** ([`time`](https://docs.python.org/3/library/datetime.html#datetime.time "(in Python v3.14)") | [`datetime`](https://docs.python.org/3/library/datetime.html#datetime.datetime "(in Python v3.14)")) – The time t can be specified as datetime.datetime, or as datetime.time in which case today is used as the date.

Return type:
[`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")

_async_ ib_async.util.timeRangeAsync(_start_, _end_, _step_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/util.html#timeRangeAsync)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.util.timeRangeAsync "Link to this definition")
Async version of [`timeRange()`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.util.timeRange "ib_async.util.timeRange").

Return type:
[`AsyncIterator`](https://docs.python.org/3/library/collections.abc.html#collections.abc.AsyncIterator "(in Python v3.14)")[[`datetime`](https://docs.python.org/3/library/datetime.html#datetime.datetime "(in Python v3.14)")]

_async_ ib_async.util.waitUntilAsync(_t_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/util.html#waitUntilAsync)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.util.waitUntilAsync "Link to this definition")
Async version of [`waitUntil()`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.util.waitUntil "ib_async.util.waitUntil").

Return type:
[`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")

ib_async.util.patchAsyncio()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/util.html#patchAsyncio)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.util.patchAsyncio "Link to this definition")
Patch asyncio to allow nested event loops.

ib_async.util.getLoop()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/util.html#getLoop)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.util.getLoop "Link to this definition")
Get asyncio event loop with smart fallback handling.

This function is designed for use in synchronous contexts or when the execution context is unknown. It will: 1. Try to get the currently running event loop (if in async context) 2. Fall back to getting the current thread’s event loop via policy 3. Create a new event loop if none exists or if the existing one is closed

For performance-critical async code paths, prefer using asyncio.get_running_loop() directly instead of this function.

Note: This function does NOT cache the loop to avoid stale loop bugs when loops are closed and recreated (e.g., in testing, Jupyter notebooks).

ib_async.util.startLoop()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/util.html#startLoop)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.util.startLoop "Link to this definition")
Use nested asyncio event loop for Jupyter notebooks.

ib_async.util.useQt(_qtLib='PyQt5'_, _period=0.01_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/util.html#useQt)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.util.useQt "Link to this definition")
Run combined Qt5/asyncio event loop.

Parameters:
*   **qtLib** ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) –

Name of Qt library to use:

    *   PyQt5

    *   PyQt6

    *   PySide2

    *   PySide6

*   **period** ([`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")) – Period in seconds to poll Qt.

ib_async.util.formatIBDatetime(_t_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/util.html#formatIBDatetime)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.util.formatIBDatetime "Link to this definition")
Format date or datetime to string that IB uses.

Return type:
[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")

ib_async.util.parseIBDatetime(_s_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/util.html#parseIBDatetime)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.util.parseIBDatetime "Link to this definition")
Parse string in IB date or datetime format to datetime.

Return type:
[`date`](https://docs.python.org/3/library/datetime.html#datetime.date "(in Python v3.14)") | [`datetime`](https://docs.python.org/3/library/datetime.html#datetime.datetime "(in Python v3.14)")

FlexReport[](https://ib-api-reloaded.github.io/ib_async/api.html#module-ib_async.flexreport "Link to this heading")
--------------------------------------------------------------------------------------------------------------------

Access to account statement webservice.

ib_async.flexreport.FLEXREPORT_URL _:[Final](https://docs.python.org/3/library/typing.html#typing.Final "(in Python v3.14)")_ _='https://ndcdyn.interactivebrokers.com/AccountManagement/FlexWebService/SendRequest?'_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.flexreport.FLEXREPORT_URL "Link to this definition")
//www.interactivebrokers.com/campus/ibkr-api-page/flex-web-service/#flex-generate-report

Type:
https

_exception_ ib_async.flexreport.FlexError[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/flexreport.html#FlexError)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.flexreport.FlexError "Link to this definition")_class_ ib_async.flexreport.FlexReport(_token=None_, _queryId=None_, _path=None_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/flexreport.html#FlexReport)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.flexreport.FlexReport "Link to this definition")
To obtain a token:

*   Login to web portal

*   Go to Settings

*   Click on “Configure Flex Web Service”

*   Generate token

Download a report by giving a valid `token` and `queryId`, or load from file by giving a valid `path`.

To overwrite default URL, set env variable `IB_FLEXREPORT_URL`.

data _:[`bytes`](https://docs.python.org/3/library/stdtypes.html#bytes "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.flexreport.FlexReport.data "Link to this definition")root _:[`Element`](https://docs.python.org/3/library/xml.etree.elementtree.html#xml.etree.ElementTree.Element "(in Python v3.14)")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.flexreport.FlexReport.root "Link to this definition")topics()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/flexreport.html#FlexReport.topics)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.flexreport.FlexReport.topics "Link to this definition")
Get the set of topics that can be extracted from this report.

extract(_topic_, _parseNumbers=True_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/flexreport.html#FlexReport.extract)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.flexreport.FlexReport.extract "Link to this definition")
Extract items of given topic and return as list of objects.

The topic is a string like TradeConfirm, ChangeInDividendAccrual, Order, etc.

Return type:
[`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")

df(_topic_, _parseNumbers=True_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/flexreport.html#FlexReport.df)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.flexreport.FlexReport.df "Link to this definition")
Same as extract but return the result as a pandas DataFrame.

get_url()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/flexreport.html#FlexReport.get_url)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.flexreport.FlexReport.get_url "Link to this definition")
Generate flexreport URL.

download(_token_, _queryId_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/flexreport.html#FlexReport.download)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.flexreport.FlexReport.download "Link to this definition")
Download report for the given `token` and `queryId`.

load(_path_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/flexreport.html#FlexReport.load)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.flexreport.FlexReport.load "Link to this definition")
Load report from XML file.

save(_path_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/flexreport.html#FlexReport.save)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.flexreport.FlexReport.save "Link to this definition")
Save report to XML file.

IBC[](https://ib-api-reloaded.github.io/ib_async/api.html#ibc "Link to this heading")
--------------------------------------------------------------------------------------

_class_ ib_async.ibcontroller.IBC(_twsVersion=0_, _gateway=False_, _tradingMode=''_, _twsPath=''_, _twsSettingsPath=''_, _ibcPath=''_, _ibcIni=''_, _javaPath=''_, _userid=''_, _password=''_, _fixuserid=''_, _fixpassword=''_, _on2fatimeout=''_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ibcontroller.html#IBC)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ibcontroller.IBC "Link to this definition")
Programmatic control over starting and stopping TWS/Gateway using IBC ([https://github.com/IbcAlpha/IBC](https://github.com/IbcAlpha/IBC)).

Parameters:
*   **twsVersion** ([_int_](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) – (required) The major version number for TWS or gateway.

*   **gateway** ([_bool_](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")) –

    *   True = gateway

    *   False = TWS

*   **tradingMode** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – ‘live’ or ‘paper’.

*   **userid** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – IB account username. It is recommended to set the real username/password in a secured IBC config file.

*   **password** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – IB account password.

*   **twsPath** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) –

Path to the TWS installation folder. Defaults:

    *   Linux: ~/Jts

    *   OS X: ~/Applications

    *   Windows: C:\Jts

*   **twsSettingsPath** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) –

Path to the TWS settings folder. Defaults:

    *   Linux: ~/Jts

    *   OS X: ~/Jts

    *   Windows: Not available

*   **ibcPath** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) –

Path to the IBC installation folder. Defaults:

    *   Linux: /opt/ibc

    *   OS X: /opt/ibc

    *   Windows: C:\IBC

*   **ibcIni** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) –

Path to the IBC configuration file. Defaults:

    *   Linux: ~/ibc/config.ini

    *   OS X: ~/ibc/config.ini

    *   Windows: %%HOMEPATH%%\DocumentsIBC\config.ini

*   **javaPath** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – Path to Java executable. Default is to use the Java VM included with TWS/gateway.

*   **fixuserid** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – FIX account user id (gateway only).

*   **fixpassword** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – FIX account password (gateway only).

*   **on2fatimeout** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – What to do if 2-factor authentication times out; Can be ‘restart’ or ‘exit’.

This is not intended to be run in a notebook.

To use IBC on Windows, the proactor (or quamash) event loop must have been set:

import asyncio
asyncio.set_event_loop(asyncio.ProactorEventLoop())

Example usage:

ibc = IBC(976, gateway=True, tradingMode='live',
    userid='edemo', password='demouser')
ibc.start()
IB.run()

IbcLogLevel _:[`ClassVar`](https://docs.python.org/3/library/typing.html#typing.ClassVar "(in Python v3.14)")_ _=10_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ibcontroller.IBC.IbcLogLevel "Link to this definition")twsVersion _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=0_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ibcontroller.IBC.twsVersion "Link to this definition")gateway _:[`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")_ _=False_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ibcontroller.IBC.gateway "Link to this definition")tradingMode _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ibcontroller.IBC.tradingMode "Link to this definition")twsPath _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ibcontroller.IBC.twsPath "Link to this definition")twsSettingsPath _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ibcontroller.IBC.twsSettingsPath "Link to this definition")ibcPath _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ibcontroller.IBC.ibcPath "Link to this definition")ibcIni _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ibcontroller.IBC.ibcIni "Link to this definition")javaPath _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ibcontroller.IBC.javaPath "Link to this definition")userid _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ibcontroller.IBC.userid "Link to this definition")password _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ibcontroller.IBC.password "Link to this definition")fixuserid _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ibcontroller.IBC.fixuserid "Link to this definition")fixpassword _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ibcontroller.IBC.fixpassword "Link to this definition")on2fatimeout _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ibcontroller.IBC.on2fatimeout "Link to this definition")start()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ibcontroller.html#IBC.start)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ibcontroller.IBC.start "Link to this definition")
Launch TWS/IBG.

terminate()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ibcontroller.html#IBC.terminate)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ibcontroller.IBC.terminate "Link to this definition")
Terminate TWS/IBG.

_async_ startAsync()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ibcontroller.html#IBC.startAsync)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ibcontroller.IBC.startAsync "Link to this definition")_async_ terminateAsync()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ibcontroller.html#IBC.terminateAsync)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ibcontroller.IBC.terminateAsync "Link to this definition")_async_ monitorAsync()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ibcontroller.html#IBC.monitorAsync)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ibcontroller.IBC.monitorAsync "Link to this definition")dict()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ibcontroller.IBC.dict "Link to this definition")
Return dataclass values as `dict`. This is a non-recursive variant of `dataclasses.asdict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ibcontroller.IBC.dict "ib_async.ibcontroller.IBC.dict")

nonDefaults()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ibcontroller.IBC.nonDefaults "Link to this definition")
For a `dataclass` instance get the fields that are different from the default values and return as `dict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ibcontroller.IBC.dict "ib_async.ibcontroller.IBC.dict")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)"), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")]

tuple()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ibcontroller.IBC.tuple "Link to this definition")
Return dataclass values as `tuple`. This is a non-recursive variant of `dataclasses.astuple`.

Return type:
[`tuple`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ibcontroller.IBC.tuple "ib_async.ibcontroller.IBC.tuple")[[`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)"), [`...`](https://docs.python.org/3/library/constants.html#Ellipsis "(in Python v3.14)")]

update(_*srcObjs_, _**kwargs_)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ibcontroller.IBC.update "Link to this definition")
Update fields of the given `dataclass` object from zero or more `dataclass` source objects and/or from keyword arguments.

Return type:
[`object`](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)")

Watchdog[](https://ib-api-reloaded.github.io/ib_async/api.html#watchdog "Link to this heading")
------------------------------------------------------------------------------------------------

_class_ ib_async.ibcontroller.Watchdog(_controller_, _ib_, _host='127.0.0.1'_, _port=7497_, _clientId=1_, _connectTimeout=2_, _appStartupTime=30_, _appTimeout=20_, _retryDelay=2_, _readonly=False_, _account=''_, _raiseSyncErrors=False_, _probeContract=Forex('EURUSD',exchange='IDEALPRO')_, _probeTimeout=4_)[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ibcontroller.html#Watchdog)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ibcontroller.Watchdog "Link to this definition")
Start, connect and watch over the TWS or gateway app and try to keep it up and running. It is intended to be used in an event-driven application that properly initializes itself upon (re-)connect.

It is not intended to be used in a notebook or in imperative-style code. Do not expect Watchdog to magically shield you from reality. Do not use Watchdog unless you understand what it does and doesn’t do.

Parameters:
*   **controller** ([_IBC_](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ibcontroller.IBC "ib_async.ibcontroller.IBC")) – (required) IBC instance.

*   **ib** ([_IB_](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ib.IB "ib_async.ib.IB")) – (required) IB instance to be used. Do not connect this instance as Watchdog takes care of that.

*   **host** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – Used for connecting IB instance.

*   **port** ([_int_](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) – Used for connecting IB instance.

*   **clientId** ([_int_](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) – Used for connecting IB instance.

*   **connectTimeout** ([_float_](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")) – Used for connecting IB instance.

*   **readonly** ([_bool_](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")) – Used for connecting IB instance.

*   **appStartupTime** ([_float_](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")) – Time (in seconds) that the app is given to start up. Make sure that it is given ample time.

*   **appTimeout** ([_float_](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")) – Timeout (in seconds) for network traffic idle time.

*   **retryDelay** ([_float_](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")) – Time (in seconds) to restart app after a previous failure.

*   **probeContract** ([_Contract_](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Contract "ib_async.contract.Contract")) – Contract to use for historical data probe requests (default is EURUSD).

*   **probeTimeout** ([_float_](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_)_ _; Timeout_ _(_ _in seconds_)

The idea is to wait until there is no traffic coming from the app for a certain amount of time (the `appTimeout` parameter). This triggers a historical request to be placed just to see if the app is still alive and well. If yes, then continue, if no then restart the whole app and reconnect. Restarting will also occur directly on errors 1100 and 100.

Example usage:

def onConnected():
    print(ib.accountValues())

ibc = IBC(974, gateway=True, tradingMode='paper')
ib = IB()
ib.connectedEvent += onConnected
watchdog = Watchdog(ibc, ib, port=4002)
watchdog.start()
ib.run()

Events:
*   `startingEvent` (watchdog: [`Watchdog`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ibcontroller.Watchdog "ib_async.ibcontroller.Watchdog"))

*   `startedEvent` (watchdog: [`Watchdog`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ibcontroller.Watchdog "ib_async.ibcontroller.Watchdog"))

*   `stoppingEvent` (watchdog: [`Watchdog`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ibcontroller.Watchdog "ib_async.ibcontroller.Watchdog"))

*   `stoppedEvent` (watchdog: [`Watchdog`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ibcontroller.Watchdog "ib_async.ibcontroller.Watchdog"))

*   `softTimeoutEvent` (watchdog: [`Watchdog`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ibcontroller.Watchdog "ib_async.ibcontroller.Watchdog"))

*   `hardTimeoutEvent` (watchdog: [`Watchdog`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ibcontroller.Watchdog "ib_async.ibcontroller.Watchdog"))

events _=['startingEvent','startedEvent','stoppingEvent','stoppedEvent','softTimeoutEvent','hardTimeoutEvent']_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ibcontroller.Watchdog.events "Link to this definition")controller _:[`IBC`](https://ib-api-reloaded.github.io/ib\_async/api.html#ib\_async.ibcontroller.IBC "ib\_async.ibcontroller.IBC")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ibcontroller.Watchdog.controller "Link to this definition")ib _:[`IB`](https://ib-api-reloaded.github.io/ib\_async/api.html#ib\_async.ib.IB "ib\_async.ib.IB")_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ibcontroller.Watchdog.ib "Link to this definition")host _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _='127.0.0.1'_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ibcontroller.Watchdog.host "Link to this definition")port _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=7497_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ibcontroller.Watchdog.port "Link to this definition")clientId _:[`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_ _=1_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ibcontroller.Watchdog.clientId "Link to this definition")connectTimeout _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=2_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ibcontroller.Watchdog.connectTimeout "Link to this definition")appStartupTime _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=30_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ibcontroller.Watchdog.appStartupTime "Link to this definition")appTimeout _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=20_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ibcontroller.Watchdog.appTimeout "Link to this definition")retryDelay _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=2_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ibcontroller.Watchdog.retryDelay "Link to this definition")readonly _:[`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")_ _=False_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ibcontroller.Watchdog.readonly "Link to this definition")account _:[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_ _=''_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ibcontroller.Watchdog.account "Link to this definition")raiseSyncErrors _:[`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")_ _=False_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ibcontroller.Watchdog.raiseSyncErrors "Link to this definition")probeContract _:[`Contract`](https://ib-api-reloaded.github.io/ib\_async/api.html#ib\_async.contract.Contract "ib\_async.contract.Contract")_ _=Forex('EURUSD',exchange='IDEALPRO')_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ibcontroller.Watchdog.probeContract "Link to this definition")probeTimeout _:[`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_ _=4_[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ibcontroller.Watchdog.probeTimeout "Link to this definition")start()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ibcontroller.html#Watchdog.start)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ibcontroller.Watchdog.start "Link to this definition")stop()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ibcontroller.html#Watchdog.stop)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ibcontroller.Watchdog.stop "Link to this definition")_async_ runAsync()[[source]](https://ib-api-reloaded.github.io/ib_async/_modules/ib_async/ibcontroller.html#Watchdog.runAsync)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ibcontroller.Watchdog.runAsync "Link to this definition")dict()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ibcontroller.Watchdog.dict "Link to this definition")
Return dataclass values as `dict`. This is a non-recursive variant of `dataclasses.asdict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ibcontroller.Watchdog.dict "ib_async.ibcontroller.Watchdog.dict")

nonDefaults()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ibcontroller.Watchdog.nonDefaults "Link to this definition")
For a `dataclass` instance get the fields that are different from the default values and return as `dict`.

Return type:
[`dict`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ibcontroller.Watchdog.dict "ib_async.ibcontroller.Watchdog.dict")[[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)"), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)")]

tuple()[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ibcontroller.Watchdog.tuple "Link to this definition")
Return dataclass values as `tuple`. This is a non-recursive variant of `dataclasses.astuple`.

Return type:
[`tuple`](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ibcontroller.Watchdog.tuple "ib_async.ibcontroller.Watchdog.tuple")[[`Any`](https://docs.python.org/3/library/typing.html#typing.Any "(in Python v3.14)"), [`...`](https://docs.python.org/3/library/constants.html#Ellipsis "(in Python v3.14)")]

update(_*srcObjs_, _**kwargs_)[](https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.ibcontroller.Watchdog.update "Link to this definition")
Update fields of the given `dataclass` object from zero or more `dataclass` source objects and/or from keyword arguments.

Return type:
[`object`](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)")

[Previous](https://ib-api-reloaded.github.io/ib_async/readme.html "ib_async")[Next](https://ib-api-reloaded.github.io/ib_async/notebooks.html "Notebooks")

* * *

 Built with [Sphinx](https://www.sphinx-doc.org/) using a [theme](https://github.com/readthedocs/sphinx_rtd_theme) provided by [Read the Docs](https://readthedocs.org/).

