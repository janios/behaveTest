Feature:
   Testing Frozen Balance

    Scenario Outline: Frozen Balance Happy Path <name>
      Given Environment, region, secret, stack and queue "<queue>"
      When I create a journal movement with account id "<account_id>", source type "<src_type>", movement type "<mvnt_type>", and amount "<amount>"
      Then The response status must be "<status>"
      When I create a frozen balance in the "<set_frozen_queue>" with source type "<frozen_src_type>", movement type "<frozen_movement_type>" and amount "<frozen_amount>"
      Then The response status must be "<status>"
      When I release a frozen balance in the "<release_frozen_queue>"  with source type "<frozen_src_type>" and "<frozen_movement_type>"
      Then The response status must be "<status>"

      Examples:
      |name           |  queue                                 | account_id                            | src_type | mvnt_type  |  amount | set_frozen_queue                            | frozen_src_type  | frozen_movement_type |  frozen_amount | release_frozen_queue                           | frozen_balance_table     |  frozen_balance_status |  frozen_balance_status_after | status |
      |Frozen Balance | payclip.service.journal.set.movements  | 884fb4a0-d066-429d-b27c-ee0136d4d2ff  |  SETT    | FAST_PYMT_RQ|  150    | payclip.service.ledger.set.frozen.balance   | PYMT             | CANCEL_RQ            |   50           | payclip.service.ledger.release.frozen.balance  | ap_ledger_frozen_balance |  PENDING               |  RELEASED_NOT_APPLIED        |  OK     |

