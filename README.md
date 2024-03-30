# 2024-Spring-HW2

Please complete the report problem below:

## Problem 1
Provide your profitable path, the amountIn, amountOut value for each swap, and your final reward (your tokenB balance).

> Path: tokenB -> tokenA -> tokenD -> tokenC -> tokenB
>
> 5.0000 tokenB  ->  5.6553 tokenA

> 5.6553 tokenA  ->  2.4588 tokenD

> 2.4588 tokenD  ->  5.0889 tokenC

> 5.0889 tokenC  ->  20.1299 tokenB
>
> Final Reward: 20.1299 tokenB

## Problem 2
What is slippage in AMM, and how does Uniswap V2 address this issue? Please illustrate with a function as an example.

> ```solidity
> function swapExactTokensForTokens(
>         uint amountIn,
>         uint amountOutMin,
>         address[] calldata path,
>         address to,
>         uint deadline
>     ) external virtual override ensure(deadline) returns (uint[] memory amounts) {
>         amounts = UniswapV2Library.getAmountsOut(factory, amountIn, path);
>         require(amounts[amounts.length - 1] >= amountOutMin, 'UniswapV2Router: INSUFFICIENT_OUTPUT_AMOUNT');
>         TransferHelper.safeTransferFrom(
>             path[0], msg.sender, UniswapV2Library.pairFor(factory, path[0], path[1]), amounts[0]
>         );
>         _swap(amounts, path, to);
>     }
> ```
>
> There is a parameter called amountOutMin, which, when checked, ensures that we receive a satisfactory amount of the target tokens. If a severe slippage situation occurs, and after all the pair swapping path, the final amount is below the amountOutMin variable, the transaction will be reverted, preventing the slippage issue.

## Problem 3
Please examine the mint function in the UniswapV2Pair contract. Upon initial liquidity minting, a minimum liquidity is subtracted. What is the rationale behind this design?

> Like any LP pool, Uniswap V2 needs defense against the “inflation attack.” Uniswap V2’s defense is to burn first MINIMUM_LIQUIDITY tokens to ensure no-one owns the entire supply of LP tokens and can easily manipulate the price. 

## Problem 4
Investigate the minting function in the UniswapV2Pair contract. When depositing tokens (not for the first time), liquidity can only be obtained using a specific formula. What is the intention behind this?

> We aim to maintain the ratio of the total supply of two tokens at a specific value. Therefore, if users provide an incorrect ratio of the two tokens, we will only consider the token with the lower ratio as the final liquidity. Additionally, any unused portion of tokens that users pass will not be returned to them. This ensures that every minter provides the correct ratio of the two tokens.

## Problem 5
What is a sandwich attack, and how might it impact you when initiating a swap?

> MEV (Maximal Extractable Value) traders will wait for a sufficiently large order to come in, then place a buy order right behind it and a sell order right after it. The leading buy order will drive up the price for the original trader, which gives them worse execution. It’s called a sandwich attack, since the victim’s trade is “sandwiched” between the attackers.
>
> 1) Attacker’s first buy (front run): drives up price for victim
>
> 2) Victim’s buy: drive up price even further
>
> 3) Attacker’s sell: sell the first buy at a profit

